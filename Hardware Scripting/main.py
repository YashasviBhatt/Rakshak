# Importing Libraries
import time
from typing_extensions import runtime
import RPi.GPIO as GPIO
from twilio.rest import Client
import requests
import json

# Setting Up GPIO Mode
GPIO.setmode(GPIO.BOARD)

# Fetching credentials from JSON
cred = open('../credentials.json')
credentials = json.load(cred)

def distance_from_object():
    '''
    Function to Calculate Distance from Object.
    Params: None
    Return: distance (Distance from Object)
    '''
    TRIG = 16                       # GPIO 23
    ECHO = 18                       # GPIO 24

    # Configuring PINs for I/O Operations
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    print('Start...')

    try:
        run = True
        while run:

            # Resetting TRIG
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            # Time when the Acoustic Signals are Transmitted
            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            # Time when Acoustic Signals are Received after hitting Object
            while GPIO.input(ECHO) == 0:
                pulse_end = time.time()

            # Time taken from transmission to receiver
            time_taken = pulse_end - pulse_start

            # D = S x T   (17150, speed of Acoustic Waves in Air)
            distance = 17150 * time_taken

            # Converting Distance in cms
            distance = round((distance + 1.15), 2)

            # Setting Up Threshold Value

            if distance >= 52:
                print('You are Safe')
                print(f'Distance : {distance} cm')
                status = deactivate()

            elif distance >= 42 and distance < 52:
                print('You are 80% Distance from Object')
                print(f'Distance : {distance} cm')
                status = deactivate()

            elif distance >= 32 and distance < 42:
                print('You are 60% Distance from Object')
                print(f'Distance : {distance} cm')
                status = deactivate()

            elif distance >= 22 and distance < 32:
                print('You are 40% Distance from Object')
                print(f'Distance : {distance} cm')
                status = deactivate()

            elif distance >= 12 and distance < 22:
                print('You are 20% Distance from Object')
                print(f'Distance : {distance} cm')
                status = open_gate()

            elif distance >= 7 and distance < 12:
                print('You are about to hit the Object')
                print(f'Distance : {distance} cm')
                status1 = open_gate()
                status2 = open_airbags()

            else:
                print('You hit the Object')
                status1 = open_gate()
                status2 = open_airbags()
                return distance

            time.sleep(2)

    except Exception as e:
        print(e)
        return False


def open_gate():
    '''
    Function to open gate of Car on Impact.
    Params: None
    Return: Status Flag (True/False)
    '''
    d1 = 29                                     # Door 1
    d2 = 31                                     # Door 2
    try:
        GPIO.setup(d1, GPIO.OUT)
        GPIO.setup(d2, GPIO.OUT)
        GPIO.output(d1, GPIO.HIGH)
        GPIO.output(d2, GPIO.HIGH)
        return True
    except Exception as e:
        print(e)
        return False


def open_airbags():
    '''
    Function to open airbags of Car on Impact.
    Params: None
    Return: Status Flag (True/False)
    '''
    a1 = 33                                     # Airbag 1
    a2 = 37                                     # Airbag 2
    try:
        GPIO.setup(a1, GPIO.OUT)
        GPIO.setup(a2, GPIO.OUT)
        GPIO.output(a1, GPIO.HIGH)
        GPIO.output(a2, GPIO.HIGH)
        return True
    except Exception as e:
        print(e)
        return False


def deactivate():
    '''
    Function to deactivate motors.
    Params: None
    Return: Status Flag (True/False)
    '''
    d1 = 29
    d2 = 31
    a1 = 33
    a2 = 37
    try:
        # Resetting Doors
        GPIO.setup(d1, GPIO.OUT)
        GPIO.setup(d2, GPIO.OUT)
        GPIO.output(d1, GPIO.LOW)
        GPIO.output(d2, GPIO.LOW)

        # Resetting Airbags
        GPIO.setup(a1, GPIO.OUT)
        GPIO.setup(a2, GPIO.OUT)
        GPIO.output(a1, GPIO.LOW)
        GPIO.output(a2, GPIO.LOW)

        return True
    except Exception as e:
        print(e)
        return False


def location():
    '''
    Function to fetch the location of the device.
    Params: None
    Return: det (Details of Device)
    '''
    try:
        # Fetching IP
        ip_addr = requests.get('https://api.ipify.org'). text

        # Fetching Details
        data = requests.get(f'ipinfo.io/{ip_addr}?token={credentials["ipinfo"]["Secret Token"]}').json()

        # Generating Data
        keys_to_fetch = ['city', 'region', 'country', 'loc', 'postal']
        final_data = []
        for ky in keys_to_fetch:
            final_data.append(data[ky])
        
        return final_data

    except Exception as e:
        print(e)
        return False


def nearby_locations():
    '''
    Function to fetch the details of Nearby Police Stations and Hospitals.
    Params: None
    Return: None
    '''
    pass


def alert(ph_num):
    '''
    Function to send Alert on Phone.
    Params: ph_num (Number on which the Alert is to be sent)
    Return: Status Flag (True/False)
    '''
    try:
        client = Client(f'{credentials["twilio"]["Access Key"]}', f'{credentials["twilio"]["Auth Token"]}')

        client.calls.create(
            twiml='<Response><Say>I have met with an Accident, the details are sent on the Mobile App</Say></Response>',
            to=f'{ph_num}',
            from_='+1'
        )

        client.messages.create(
            body='Please help I have met with an accident.',
            to=f'{ph_num}',
            from_='+1'
        )

        return True

    except Exception as e:
        print(e)
        return False


def store_data(city, region, country, postal_code, latitude, longitude):
    '''
    Function to store data on Firebase.
    Params: city, region, country, postal_code, latitude, longitude
    Return: Status Flag (True/False)
    '''
    try:
        url = f'{credentials["firebase"]["DBurl"]}/yashasvibhatt.json'
        data = f'''
        {{
            "city": "{city}",
            "country": "{country}",
            "postal_code": "{postal_code}",
            "latitude": "{latitude}",
            "longitude": "{longitude}",
            "region": "{region}"
        }}
        '''
        response = requests.patch(url=url, data=data)
        if response.status_code == 200:
            return True
        else:
            return False
    
    except Exception as e:
        print(e)
        return False


def main():
    '''
    Driver Function.
    Params: None
    Return: Status Flag (True)
    '''
    # Fetching Distance
    distance = distance_from_object()
    if distance:

        # Fetching Location
        det = location()
        if det:
            city = det[0]
            region = det[1]
            country = det[2]
            postal_code = det[4]
            latitude = str(det[3]).split(',')[0]
            longitude = str(det[3]).split(',')[1]

            # Fetch Nearby details of Police Stations and Hospitals
            # n_hos, n_pol = nearby_locations()

            # Sending Alert
            status = alert('+918107585499')

            # Storing Data
            status = store_data(city, region, country, postal_code, latitude, longitude)

            return True

# Driver Code
if __name__ == '__main__':
    main()
    GPIO.cleanup()                          # cleaning GPIO