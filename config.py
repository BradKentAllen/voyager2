#!/usr/bin/env python
# -*- coding: utf-8 -*-
# config.py for Modem_Rider
#!/usr/bin/env python
'''
file name: Modem_Rider_config.py
date created: July 10, 2022
created by: Brad Allen
project/support: Modem Rider (voyager2) # root or script it supports
description:

special instruction:
'''
__revision__ = 'v0.0.2'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'


    ################################
    #### (1.0) General Settings ####
    ################################

#### (1.2) # Time Zone
local_time_zone = 'US/Pacific'

# XXXX for UTC: 
# 'US/Aleutian', 'US/Hawaii', 'US/Alaska', 'US/Arizona', 'US/Michigan'
# 'US/Pacific', 'US/Mountain', 'US/Central', 'US/Eastern'


#### (1.3) # Polling Rate
# RPi_voyager polls for systems on a set rate. Typically this is 100 milliseconds
# If you have every poll timers that take more than the poll time, you can increase this
# up to 999 millis
# Polling faster than 10 hz is possible but you will start losing polling operations at some point
POLL_MILLIS = 100


# If DEBUG = True
# For use when testing RPi using command line
# Will give results in print statements for locating issues
# During config file validation, results are printed not sent to LCD and each error will stop
# operation and raise a ConfigValueError.
DEBUG = True


#### (1.3) # Communicatio Interfaces (USB and WIFI)
# In order to use USB drives, must have set up RPi with usbmount
# This includes installing usbmount and modifying /lib/systemd/system/systemd-udevd.service
USB_MOUNT = False

# wifi_auto moves the RPi wpa_supplicant from USB to the drive then to use for wifi
# usb_mount must be True for this to work, as a USB drive is required
WIFI_AUTO = True



    ##############################
    #### (2.0) Hardware Setup ####
    ##############################

#### (2.1) # RPi pins
# RPi_voyager uses the BCM pin numbering nomenclature
# BCM corresponds to the processor, not the RPi board
# These are non-sequentially numbered pins on most diagrams

RPi_PINOUT_BCM = {
    'red_LED': 5,
    'yellow_LED': 11,   # on Jim Hawkins board
    'blue_LED_1': 9,    # on Jim Hawkins board
    'blue_LED_2': 10,   # on Jim Hawkins board

    # these are customizable
    # availabe types:  'LED', 'Output'

        # Header 1 (by power jack, 6-pin) ONLY 4-PIN on Modem Rider
    'i_o_4': {'name': 'button_1', 'type': 'Button', 'pin': 14}, # Jim Hawkins, header 1, pin 1
    'i_o_5': {'name': 'button_2', 'type': 'Button', 'pin': 15}, # Jim Hawkins, header 1, pin 2
    'i_o_8': {'name': 'button_3', 'type': 'Button', 'pin': 18}, # Jim Hawkins, header 1, pin 3
    'i_o_23': {'name': 'modem', 'type': 'Output', 'pin': 23}, # Jim Hawkins, header 1, pin 5
    'i_o_24': {'name': 'router', 'type': 'Output', 'pin': 24}, # Jim Hawkins, header 1, pin 6

        # Header 2 (on left side by i/o, 6-pin)
    'i_o_12': {'name': 'cycling_LED', 'type': 'LED', 'pin': 12},  # Jim Hawkins, header 2, pin 3
    'i_o_16': {'name': 'Internet_Bad_LED', 'type': 'LED', 'pin': 16},  # Jim Hawkins, header 2, pin 4
    'i_o_20': {'name': 'Internet_Good_LED', 'type': 'LED', 'pin': 20},   # Jim Hawkins, header 2, pin 5
    
}

#### (2.2) # RPi GPIO
# pigpio is an alternative control for the RPi gpio
# pigpio provides more stable hardware pulse width modulations
# when using servos
# The pigpio daemon must be running for this to work
# To enable and will run on boot:
# sudo systemctl enable pigpiod
USE_PIGPIO = False


    ##################################
    #### 3.0 UI, Buttons, Display ####
    ##################################

#### (3.1) # LCD setup
# 'I2C/16x2', 'I2C/20x4', 'wired/16x2', None
LCD_TYPE = 'I2C/16x2'
I2C_LCD_ADDRESS = 0x27
BACKLIGHT_OFF_TIME = 3  # minutes until backlight goes off

custom_chars = {
    'GPS': 0,
    'down arrow': 3,
    'water drop': 1,
    'up arrow': 2,
    }

#### (3.2) # Buttons
# button pullup is True if button connects input to ground
# button pullup is False if button connects input to 3V3
button_pull_up = False

# button hold time is used for time it takes to hold a button for a function
button_hold_time = 2


#### (3.3) # Display Scroll Interface
# this is the source for all material put on LCD display



    #####################################################
    #### (4.0) Sensors, Data, Data Recorder, Logging ####
    #####################################################
#### (4.1) # Sensor List 
# select from Available Sensors in list below for this machine
# full senosr details are in the documentation
# some sensors use Adafruit drivers which must be individually loaded
SENSOR_LIST = ['HIH6121', ]

# (4.1.1) Available sensors on this machine:
# 'HIH6121' - Honeywell tempurature and RH
HIH6121_I2C_address = 0x27  # this is probably 0x27

#### (4.2) # Units
UNITS_TEMP = 'F'    # 'F' or 'C'

# saves data and recovers when restarts
# can be False or an integer number of minutes
# number of minutes is how often the data is saved
SAVE_BETWEEN_SESSIONS = 10

# data logger
data_file_name = 'data_log'
DATA_FILE_TITLE = 'Alarm Clock Data'
RECORD_DATA = 'all'     # all or list of data parameter names and their titles {'RH': 'RH', 'tempF': 'F', 'tempC': 'C'} 
RECORD_CSV = False
RECORD_TXT = True
RECORD_TO_SD = True
RECORD_TO_USB = False

# file manage mode can be: 'one file/keep all', 'one file/record over', 'new file each run'
FILE_MANAGE_MODE = 'one file/keep all'
FILE_LINE_LIMIT = 10    # only keeps last ten lines
DAILY_HEADER = False

# data logger formatting (primarily for .txt file)
TIME_SPACE = 12     # Space allotted for time column

# details for each type of data to be recorded
# Name is official name for that data and must be available from an active sensor
# Tuple format:  ('column title, number of spaces for column as integer)
DATA_RECORD_DETAILS = {
    'RH': ('RH', 5), 
    'temp': (UNITS_TEMP, 8),
    } 



    ###############################
    #### (5.0) Output Hardware ####
    ###############################
####



    ########################################
    #### 6.0 Unique Function Parameters ####
    ########################################
####
#### Weather
phoneBrad = '14259856203'
phoneAnn = '14254171516'

# for checking Internet status
check_URL1 = 'http://google.com'
check_URL2 = 'https://gtmetrix.com'
URL_timeout = 10

# for cycling modem and router
DEVICE_OFF_TIME = 15    # seconds modem and router are off initially
# XXX - don't need? WIFI_ROUTER_DELAY = 15  # seconds after modem is powered on before wifi power
WAIT_TO_CHECK_INTERNET = 60 # seconds after wifi is on before starting to check












