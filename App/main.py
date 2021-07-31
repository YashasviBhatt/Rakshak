from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import json
import requests
from passlib.hash import sha256_crypt
from datetime import datetime
import os

# Fetching credentials from JSON
with open('../credentials.json') as cred:
    credentials = json.load(cred)

# Fetching Login Credentials for Rapid Login
with open('./log_credentials.json') as log_cred:
    log_credentials = json.load(log_cred)

# Fetching Data from Database
url = f'{credentials["firebase"]["DBurl"]}.json'
db_data = requests.get(url=url).json()

# Storing User Details
global user_data

# Layout String
layout_string = '''


#:import MapView kivy_garden.mapview.MapView

# Registerting Screens on ScreenManager
ScreenManager:
    Home:
    Register:
    Login:
    Dashboard:
    Location:
    Weather:
    Docs:
    Stats:
    GovNaB:
    PrivacyPolicy:
    Profile:
    About:
    AboutRakshak:
    AboutUs:
    Person1:
    Person2:
    Person3:
    College:
    TrafficRules:
    Contact:


# Home Screen Layout Configurations
<Home>:
    name: 'HomeScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding Toolbar to Home Screen
    MDToolbar:
        title: 'Rakshak'
        pos_hint: {'top': 1}
        md_bg_color: app.appbarcolor
        elevation: 10

    # Adding Background Image to Home Screen
    Image:
        source: './images/home_background.jpeg'
        pos_hint: {'center_x': .5, 'center_y': .66}
        size_hint: None, None
        size: '150dp', '150dp'

    # Adding Register Button to Home Screen
    MDFillRoundFlatIconButton:
        pos_hint: {'center_x': .5, 'center_y': .4}
        icon: 'login'
        text: 'Register'
        md_bg_color: app.buttoncolor
        width: '200dp'

        # Adding Functionality to Button
        on_release:
            root.manager.current = 'RegisterScreen'
            root.manager.transition.direction = 'left'

    # Adding Login Button to Home Screen
    MDFillRoundFlatIconButton:
        pos_hint: {'center_x': .5, 'center_y': .3}
        icon: 'login-variant'
        text: '   Login    '
        md_bg_color: app.buttoncolor
        width: '200dp'

        # Adding Functionality to Button
        on_release:
            root.manager.current = 'LoginScreen'
            root.manager.transition.direction = 'left'


# Register Screen Layout Configurations
<Register>:
    name: 'RegisterScreen'

    # Creating ID Instances of Input IDs for value access in main program
    register_name: register_name
    register_phone: register_phone
    register_email: register_email
    register_username: register_username
    register_password: register_password

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding Toolbar to Register Screen
    MDToolbar:
        title: 'Rakshak Registration'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    # Adding Background Image to Register Screen
    Image:
        source: './images/register_background.jpeg'
        pos_hint: {'center_x': .5, 'center_y': .7}
        size_hint: None, None
        size: '150dp', '150dp'

    # Text Field for Name Input
    MDTextFieldRound:
        id: register_name
        icon_left: 'account-box'
        normal_color: 0, 128/255, 128/255, 0.3
        color_active: 0, 128/255, 128/255, 1
        hint_text: 'Enter Name'
        font_size: '16dp'
        write_tab: False
        multiline: False
        current_hint_text_color: 1, 0, 1, 1
        size_hint_x: 0.8
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

    # Text Field for Phone Input
    MDTextFieldRound:
        id: register_phone
        icon_left: 'phone'
        normal_color: 0, 128/255, 128/255, 0.3
        color_active: 0, 128/255, 128/255, 1
        hint_text: 'Enter Phone Number'
        font_size: '16dp'
        write_tab: False
        multiline: False
        size_hint_x: 0.8
        pos_hint: {'center_x': 0.5, 'center_y': 0.43}

    # Text Field for Email Input
    MDTextFieldRound:
        id: register_email
        icon_left: 'email'
        normal_color: 0, 128/255, 128/255, 0.3
        color_active: 0, 128/255, 128/255, 1
        hint_text: 'Enter Email'
        font_size: '16dp'
        write_tab: False
        multiline: False
        size_hint_x: 0.8
        pos_hint: {'center_x': 0.5, 'center_y': 0.36}

    # Text Field for Re-Type Password Input
    MDTextFieldRound:
        id: register_username
        icon_left: 'account'
        normal_color: 0, 128/255, 128/255, 0.3
        color_active: 0, 128/255, 128/255, 1
        hint_text: 'Enter Username'
        font_size: '16dp'
        write_tab: False
        multiline: False
        size_hint_x: 0.8
        pos_hint: {'center_x': 0.5, 'center_y': 0.29}

    # Text Field for Password Input
    MDTextFieldRound:
        id: register_password
        icon_left: 'key-variant'
        icon_right: 'eye'
        normal_color: 0, 128/255, 128/255, 0.3
        color_active: 0, 128/255, 128/255, 1
        hint_text: 'Enter Password'
        font_size: '16dp'
        write_tab: False
        multiline: False
        password: True
        size_hint_x: 0.8
        pos_hint: {'center_x': 0.5, 'center_y': 0.22}

    # Button to Hide/Show Password
    MDIconButton:
        icon: 'eye'
        user_font_size: '20dp'
        theme_text_color: 'Custom'
        text_color: 1, 1, 1, 0
        pos_hint: {'center_x': .885, 'center_y': .22}

        # Adding on_release event
        on_release: 
            root.password_display()

    # Adding Register Button to Register Screen
    MDFillRoundFlatIconButton:
        pos_hint: {'center_x': .5, 'center_y': .12}
        icon: 'login'
        text: 'Register'
        md_bg_color: app.buttoncolor
        width: '200dp'

        # Adding on_release event
        on_release: 
            root.verify_credentials()


# Login Screen Layout Configurations
<Login>:
    name: 'LoginScreen'

    # Creating ID Instances of Input IDs for value access in main program
    login_username: login_username
    login_password: login_password

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding Toolbar to Login Screen
    MDToolbar:
        title: 'Rakshak Login'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    # Adding Background Image to Login Screen
    Image:
        source: './images/login_background.jpeg'
        pos_hint: {'center_x': .5, 'center_y': .7}
        size_hint: None, None
        size: '150dp', '150dp'

    # Text Field for Username Input
    MDTextFieldRound:
        id: login_username
        icon_left: 'account'
        normal_color: 0, 128/255, 128/255, 0.3
        color_active: 0, 128/255, 128/255, 1
        hint_text: 'Enter Username'
        font_size: '16dp'
        write_tab: False
        multiline: False
        size_hint_x: 0.8
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    
    # Text Field for Password Input
    MDTextFieldRound:
        id: login_password
        icon_left: 'key-variant'
        icon_right: 'eye'
        normal_color: 0, 128/255, 128/255, 0.3
        color_active: 0, 128/255, 128/255, 1
        hint_text: 'Enter Password'
        font_size: '16dp'
        write_tab: False
        multiline: False
        password: True
        size_hint_x: 0.8
        pos_hint: {'center_x': 0.5, 'center_y': 0.43}

    # Button to Hide/Show Password
    MDIconButton:
        icon: 'eye'
        user_font_size: '20dp'
        theme_text_color: 'Custom'
        text_color: 1, 1, 1, 0
        pos_hint: {'center_x': .885, 'center_y': .43}

        # Adding on_release event
        on_release: 
            root.password_display()

    # Adding Login Button to Login Screen
    MDFillRoundFlatIconButton:
        pos_hint: {'center_x': .5, 'center_y': .33}
        icon: 'login-variant'
        text: '   Login    '
        md_bg_color: app.buttoncolor
        width: '200dp'

        # Adding on_release event
        on_release: 
            root.check_credentials()


# Dashboard Screen Layout Configurations
<Dashboard>:
    name: 'UserDashboard'

    # Creating ID Instances of Input IDs for value access in main program
    user_name: user_name
    user_avatar: user_avatar
    user_username: user_username

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
        
    # Adding Lines
    canvas:
        Color:
            rgba: 0, 128/255, 128/255, 0.5
        # Line:
        #     points: self.width / 2, 20, self.width / 2, self.height - 20 - 64       # Toolbar Height
        # Line:
        #     points: 20, (self.height - 64) / 2, self.width - 20, (self.height - 64) / 2

        Line:
            points: self.width / 2, self.height / 10, self.width / 2, (self.height - 64) / 2 - self.height / 10
        Line:
            points: self.width / 2, self.height - 64 - self.height / 10, self.width / 2, (self.height - 64) / 2 + self.height / 10
        Line:
            points: (self.width / 10), (self.height - 64) / 2, (self.width / 2) - (self.width / 10), (self.height - 64) / 2
        Line:
            points: (self.width / 2) + (self.width / 10), (self.height - 64) / 2, self.width - (self.width / 10), (self.height - 64) / 2

    # Adding Toolbar to Dashboard Screen
    MDToolbar:
        title: 'Rakshak Dashboard'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['menu', lambda nav: nav_drawer.set_state('toggle')]]

    # Button to Navigate to Location Screen
    Button:
        background_normal: './images/location_logo_up.png'
        background_down: './images/location_logo_down.png'
        size_hint: 0.34, 0.34
        pos_hint: {'center_x': 0.25, 'center_y': 0.65}
        on_release: 
            root.manager.current = 'LocationMapView'
            root.manager.transition.direction = 'left'
    
    # Button to Navigate to Weather Screen
    Button:
        background_normal: './images/weather_logo_up.jpg'
        background_down: './images/weather_logo_down.jpg'
        size_hint: 0.34, 0.2
        pos_hint: {'center_x': 0.75, 'center_y': 0.65}
        on_release: 
            root.manager.current = 'WeatherScreen'
            root.manager.transition.direction = 'left'

    # Button to Navigate to Documents Screen
    Button:
        background_normal: './images/documents_logo_up.png'
        background_down: './images/documents_logo_down.png'
        size_hint: 0.34, 0.28
        pos_hint: {'center_x': 0.25, 'center_y': 0.25}
        on_release: 
            root.manager.current = 'DocsScreen'
            root.manager.transition.direction = 'left'

    # Button to Navigate to Stats Screen
    Button:
        background_normal: './images/stats_logo_up.png'
        background_down: './images/stats_logo_down.png'
        size_hint: 0.34, 0.2
        pos_hint: {'center_x': 0.75, 'center_y': 0.25}
        on_release: 
            root.manager.current = 'StatsScreen'
            root.manager.transition.direction = 'left'

    # Adding Navigation Drawer to Dashboard Screen
    MDNavigationDrawer:
        id: nav_drawer
        
        # Changing Background
        canvas:
            Color:
                rgba: 0, 128/255, 128/255, 0.5
            Rectangle:
                pos: self.pos
                size: self.size

        # Rendering Content to Navigation Drawer
        BoxLayout:
            orientation: 'vertical'
            padding: '8dp'
            spacing: '8dp'

            # Displaying Image of User 
            AnchorLayout:
                anchor_x: 'left'
                size_hint_y: None
                height: user_avatar.height

                # Rendering Online Image
                AsyncImage:
                    id: user_avatar
                    size_hint: None, None
                    size: '100dp', '100dp'
                    source: 'https://upload.wikimedia.org/wikipedia/commons/5/58/Kivy_logo.png'
            
            # Displaying Name of User
            MDLabel:
                id: user_name
                text: 'Name'
                font_style: 'Button'
                size_hint_y: None
                height: self.texture_size[1]
            
            # Displaying Username of User
            MDLabel:
                id: user_username
                text: 'Username'
                font_style: 'Caption'
                size_hint_y: None
                height: self.texture_size[1]

            # Adding Scroll Action to List
            ScrollView:

                # Adding Navigation Button
                MDList:
                    TwoLineAvatarIconListItem:
                        text: 'GovNaB'
                        secondary_text: 'Your AI Bot'
                        on_release:
                            root.manager.current = 'ChatBotScreen'
                            root.manager.transition.direction = 'left'
                        IconLeftWidget:
                            icon: 'robot-happy-outline'
                            on_release:
                                root.manager.current = 'ChatBotScreen'
                                root.manager.transition.direction = 'left'
                    OneLineIconListItem:
                        text: 'Privacy Policy'
                        on_release:
                            root.manager.current = 'PrivacyScreen'
                            root.manager.transition.direction = 'left'
                        IconLeftWidget:
                            icon: 'security'
                            on_release:
                                root.manager.current = 'PrivacyScreen'
                                root.manager.transition.direction = 'left'
                    OneLineIconListItem:
                        text: 'Profile'
                        on_release:
                            root.manager.current = 'ProfileScreen'
                            root.manager.transition.direction = 'left'
                        IconLeftWidget:
                            icon: 'account-edit'
                            on_release:
                                root.manager.current = 'ProfileScreen'
                                root.manager.transition.direction = 'left'
                    OneLineIconListItem:
                        text: 'About'
                        on_release:
                            root.manager.current = 'AboutScreen'
                            root.manager.transition.direction = 'left'
                        IconLeftWidget:
                            icon: 'package'
                            on_release:
                                root.manager.current = 'AboutScreen'
                                root.manager.transition.direction = 'left'
                    OneLineIconListItem:
                        text: 'Traffic Rules'
                        on_release:
                            root.manager.current = 'TrafficRulesScreen'
                            root.manager.transition.direction = 'left'
                        IconLeftWidget:
                            icon: 'list-status'
                            on_release:
                                root.manager.current = 'TrafficRulesScreen'
                                root.manager.transition.direction = 'left'
                    OneLineIconListItem:
                        text: 'Contact Us'
                        on_release:
                            root.manager.current = 'ContactScreen'
                            root.manager.transition.direction = 'left'
                        IconLeftWidget:
                            icon: 'email-send'
                            on_release:
                                root.manager.current = 'ContactScreen'
                                root.manager.transit
                    OneLineIconListItem:
                        text: 'Logout'
                        on_release: 
                            root.logout()
                        IconLeftWidget:
                            icon: 'logout'


# Location MapView Screen Layout Configurations
<Location>:
    name: 'LocationMapView'

    # Creating ID Instances of Input IDs for value access in main program
    map_view: map_view
    map_marker: map_marker

    # Adding MapView to render location
    MapView:
        id: map_view
        lat: 0
        lon: 0
        zoom: 15
        double_tap_zoom: True

        # Adding Map Marker
        MapMarkerPopup:
            id: map_marker
            source: './images/marker.png'
            size: '40dp', '40dp'
            lat: 0
            lon: 0

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Location'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    # Adding ToolBar to Screen
    MDToolbar:
        title: ''
        pos_hint: {'top': 0.875}
        elevation: 10
        md_bg_color: 1, 1, 1, 1
        height: '30dp'
    
    MDFloatingActionButton:
        icon: 'map-marker'
        md_bg_color: app.buttoncolor
        pos_hint: {'center_x': 0.85, 'center_y': 0.15}
        on_release:
            root.fetch_latest_loc()
            map_view.center_on(root.lat, root.lon)
    
    MDLabel:
        text: 'Lat - {0:.4f} : Lon - {1:.4f}'.format(map_marker.lat, map_marker.lon)
        pos_hint: {'center_y': 0.85}
        halign: 'center'
        font_size: '16dp'
        

# Weather Screen Layout Configurations
<Weather>:
    name: 'WeatherScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Weather'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


# Docs Screen Layout Configurations
<Docs>:
    name: 'DocsScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Documents'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


# Stats Screen Layout Configurations
<Stats>:
    name: 'StatsScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Statistics'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


# ChatBot Screen Layout Configurations
<GovNaB>:
    name: 'ChatBotScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'GovNaB'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


<PrivacyPolicy>:
    name: 'PrivacyScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Privacy Policy'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}

<Profile>:
    name: 'ProfileScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Profile'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


<About>:
    name: 'AboutScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'About'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}
    

<AboutRakshak>:
    name: 'AboutProjectScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'About Rakshak'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}
    

<AboutUs>:
    name: 'AboutUsScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'About Us'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}
    

<Person1>:
    name: 'Person1Screen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Yashasvi Bhatt'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


<Person2>:
    name: 'Person2Screen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Yashvardhan Goel'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


<Person3>:
    name: 'Person3Screen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Dinesh Verma'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}
    

<College>:
    name: 'CollegeScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'GIT'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


<TrafficRules>:
    name: 'TrafficRulesScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Traffic Rules'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


<Contact>:
    name: 'ContactScreen'

    # Clearing Screen
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Adding ToolBar to Screen
    MDToolbar:
        title: 'Contact Us'
        pos_hint: {'top': 1}
        elevation: 10
        md_bg_color: app.appbarcolor
        left_action_items: [['arrow-left', lambda scr: root.previous()]]

    MDLabel:
        text: 'Coming Soon'
        halign: 'center'
        font_style: 'H2'
        pos_hint: {'center_y': 0.5}


'''

class Home(Screen):
    def on_enter(self, *args):
        global user_data
        if log_credentials['username'] == '':
            pass
        else:
            username = log_credentials['username']
            password = log_credentials['password']
            date = log_credentials['date']
            curr = str(datetime.now()).split()[0]
            today = datetime.strptime(curr, '%Y-%m-%d')
            prev = datetime.strptime(date, '%Y-%m-%d')
            nod = today - prev
            if nod.days <= 3:
                if username in db_data.keys():
                    user_data = db_data[username]
                    if sha256_crypt.verify(password, user_data['password']):
                        Clock.schedule_once(self.callback, 0)
    
    def callback(self, dt):
        self.manager.current = 'UserDashboard'


class Register(Screen):
    def verify_credentials(self):
        if self.register_name.text == '' or self.register_phone.text == '' or self.register_email.text == '' or self.register_username.text == '' or self.register_password.text == '':
            self.dialog_empty_fields = MDDialog(
                text='Fill All Fields',
                buttons=[
                    MDFlatButton(
                        text='OK', 
                        on_release=lambda _:self.dialog_empty_fields.dismiss()
                    ),
                ],
            )
            self.dialog_empty_fields.open()
        else:
            if self.register_username.text in db_data.keys():
                self.dialog_already_exists = MDDialog(
                    text='Username Already Taken',
                    buttons=[
                        MDFlatButton(
                            text='OK', 
                            on_release=lambda _:self.dialog_already_exists.dismiss()
                        ),
                    ],
                )
                self.dialog_already_exists.open()

                self.register_username.text = ''
                self.register_passsword.text = ''
            else:
                data_to_store = f'''
                {{
                    "{self.register_username.text}": {{
                        "email": "{self.register_email.text}",
                        "password": "{sha256_crypt.hash(self.register_password.text)}",
                        "name": "{self.register_name.text}",
                        "phone": "{self.register_phone.text}",
                        "city": "",
                        "region": "",
                        "country": "",
                        "latitude": "",
                        "longitude": "",
                        "postal_code": "",
                        "status": false,
                        "activate": false
                    }}
                }}
                '''
                res = requests.patch(url=url, data=data_to_store)
                print(res)

                self.log_cred = open('./log_credentials.json', 'w')
                self.username = self.register_username.text
                self.password = self.register_password.text
                self.log_credentials = {
                    'username': self.username,
                    'password': self.password,
                    'date': str(datetime.now()).split()[0]
                }
                json.dump(self.log_credentials, self.log_cred)
                self.log_cred.close()

                self.manager.current = 'UserDashboard'

    def password_display(self):
        if self.register_password.text == '':
            self.register_password.password = True
            self.register_password.icon_right = 'eye'
        else:
            self.register_password.password = not self.register_password.password
            if self.register_password.password:
                self.register_password.icon_right = 'eye'
            else:
                self.register_password.icon_right = 'eye-off'

    def previous(self):
        self.manager.current = 'HomeScreen'
        self.manager.transition.direction = 'right'


class Login(Screen):
    global user_data
    def check_credentials(self):
        if self.login_username.text == '' or self.login_password.text == '':
            self.dialog_empty_fields = MDDialog(
                text='Fill All Fields',
                buttons=[
                    MDFlatButton(
                        text='OK', 
                        on_release=lambda _:self.dialog_empty_fields.dismiss()
                    ),
                ],
            )
            self.dialog_empty_fields.open()
        else:
            self.dialog_invalid_credentials = MDDialog(
                text='Invalid Username or Password',
                buttons=[
                    MDFlatButton(
                        text='OK', 
                        on_release=lambda _:self.dialog_invalid_credentials.dismiss()
                    ),
                ],
            )
            if self.login_username.text in db_data.keys():
                user_data = db_data[self.login_username.text]
                if sha256_crypt.verify(self.login_password.text, user_data['password']):
                    self.log_cred = open('./log_credentials.json', 'w')
                    self.username = self.login_username.text
                    self.password = self.login_password.text
                    self.log_credentials = {
                        'username': self.username,
                        'password': self.password,
                        'date': str(datetime.now()).split()[0]
                    }
                    json.dump(self.log_credentials, self.log_cred)
                    self.log_cred.close()

                    self.manager.current = 'UserDashboard'
                else:
                    self.dialog_invalid_credentials.open()
                    self.login_password.text = ''
            else:
                self.dialog_invalid_credentials.open()
                self.login_password.text = ''

    def password_display(self):
        if self.login_password.text == '':
            self.login_password.password = True
            self.login_password.icon_right = 'eye'
        else:
            self.login_password.password = not self.login_password.password
            if self.login_password.password:
                self.login_password.icon_right = 'eye'
            else:
                self.login_password.icon_right = 'eye-off'

    def previous(self):
        self.manager.current = 'HomeScreen'
        self.manager.transition.direction = 'right'


class Dashboard(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callback, 0)
    
    def callback(self, dt):
        try:
            self.user_name.text = f" {user_data['name']}"
            self.user_username.text = f" {log_credentials['username']}"
        except Exception as e:
            Clock.schedule_once(self.callback, 0)

    def logout(self):
        self.log_cred = open('./log_credentials.json', 'w')
        self.log_credentials = {
            'username': '',
            'password': '',
            'date': ''
        }
        json.dump(self.log_credentials, self.log_cred)
        self.log_cred.close()
        log_credentials['username'] = ''
        log_credentials['password'] = ''
        log_credentials['date'] = ''
        self.manager.current = 'LoginScreen'
        self.manager.transition.direction = 'right'


class Location(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callback, 0)
    
    def callback(self, dt):
        try:
            self.map_view.lat, self.map_view.lon = self.loc()
            self.map_marker.lat, self.map_marker.lon = self.loc()
            self.map_view.center_on(self.lat, self.lon)
        except Exception as e:
            Clock.schedule_once(self.callback, 0)   

    def loc(self):
        lat = 0
        lon = 0
        try:
            self.lat = float(user_data['latitude'])
            self.lon = float(user_data['longitude'])
        except:
            # Displaying Mobile Location

            # Fetching IP
            ip_addr = requests.get('https://api.ipify.org').text

            # Fetching Details
            data = requests.get(f'https://ipinfo.io/{ip_addr}?token={credentials["ipinfo"]["Secret Token"]}').json()

            # Fetching Latitude and Longitude
            self.lat = float(data['loc'].split(',')[0])
            self.lon = float(data['loc'].split(',')[1])
        finally:
            return self.lat, self.lon

    def fetch_latest_loc(self):
        # Fetching Data from Database
        url = f'{credentials["firebase"]["DBurl"]}.json'
        db_data = requests.get(url=url).json()
        # Fetching Login Credentials for Rapid Login
        with open('./log_credentials.json') as log_cred:
            log_credentials = json.load(log_cred)
        user_new_data = db_data[log_credentials['username']]
        try:
            self.lat = float(user_new_data['latitude'])
            self.lon = float(user_new_data['longitude'])
        except:
            # Displaying Mobile Location

            # Fetching IP
            ip_addr = requests.get('https://api.ipify.org').text

            # Fetching Details
            data = requests.get(f'https://ipinfo.io/{ip_addr}?token={credentials["ipinfo"]["Secret Token"]}').json()

            # Fetching Latitude and Longitude
            self.lat = float(data['loc'].split(',')[0])
            self.lon = float(data['loc'].split(',')[1])
        finally:
            self.map_marker.lat, self.map_marker.lon = self.lat, self.lon
            self.map_view.center_on(self.lat, self.lon)

    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'


class Weather(Screen):
    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'


class Docs(Screen):
    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'


class Stats(Screen):
    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'


class GovNaB(Screen):
    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'
    
    
class PrivacyPolicy(Screen):
    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'


class Profile(Screen):
    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'


class About(Screen):
    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'


class AboutRakshak(Screen):
    pass


class AboutUs(Screen):
    pass


class Person1(Screen):
    pass


class Person2(Screen):
    pass


class Person3(Screen):
    pass


class College(Screen):
    pass


class TrafficRules(Screen):
    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'


class Contact(Screen):
    def previous(self):
        self.manager.current = 'UserDashboard'
        self.manager.transition.direction = 'right'


class RakshakApp(MDApp):
    def build(self):
        self.appbarcolor = [0, 128/255, 128/255, 1]
        self.buttoncolor = [0, 128/255, 128/255, 1]
        screen = Screen()
        app_layout = Builder.load_string(layout_string)
        screen.add_widget(app_layout)
        return screen


if __name__ == '__main__':
    Window.size = (300, 500)
    scr_mgr = ScreenManager()
    scr_mgr.add_widget(Home(name='HomeScreen'))
    scr_mgr.add_widget(Dashboard(name='UserDashboard'))
    RakshakApp().run()