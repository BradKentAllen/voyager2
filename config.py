#!/usr/bin/env python
# -*- coding: utf-8 -*-
# config.py for Life Tester A
'''
file name: config.py
date created: October 5, 2022
created by: Brad Allen
project/support: Life Tester A (voyager2) # root or script it supports
description:

special instruction:
'''
__project_name__ = "Life Tester"
__revision__ = 'v1.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'


    ################################
    #### (1.0) General Settings ####
    ################################

# #### (1.0) Test Settings
CAN_PASS_UP_SWITCH = False
CAN_PASS_DOWN_SWITCH = False

# #### (1.1) File structure
DATA_DIR = "data"
LIFE_CYCLES_FILENAME = "life_cycles"

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
# IMPORTANT:  DEBUG disables the try/except in except-safe.  This means faults will not
# clean up the gpio and outputs will stay on if on at exception or keyboard interrupt.
# Will give results in print statements for locating issues
DEBUG = False




    ##############################
    #### (2.0) Hardware Setup ####
    ##############################

#### (2.1) # RPi pins
# RPi_voyager uses the BCM pin numbering nomenclature
# BCM corresponds to the processor, not the RPi board
# These are non-sequentially numbered pins on most diagrams

RPi_PINOUT_BCM = {
    'red_LED': 5,
    'green_LED': 11,   # on Jim Hawkins board
    'blue_LED_1': 9,    # on Jim Hawkins board
    'blue_LED_2': 10,   # on Jim Hawkins board

    # these are customizable
    # availabe types:  'LED', 'Button', Output'
    # these must match the available i/o in v2_gpio.py

        # Header 1 (by power jack, 6-pin) ONLY 4-PIN on Modem Rider
    "Header 1 - pin 3": {'name': 'UP_relay', 'type': 'LED', 'pin': 26}, # Jim Hawkins, header 1, pin 3
    "Header 1 - pin 4": {'name': 'DOWN_relay', 'type': 'LED', 'pin': 15}, # Jim Hawkins, header 1, pin 4
    "Header 1 - pin 5": {'name': 'up_switch', 'type': 'Button', 'pin': 18}, # Jim Hawkins, header 1, pin 5
    "Header 1 - pin 6": {'name': 'down_switch', 'type': 'Button', 'pin': 23}, # Jim Hawkins, header 1, pin 6
    "Header 1 - pin 7": {'name': 'input3', 'type': 'Button', 'pin': 24}, # Jim Hawkins, header 1, pin 7

        # Header 2 (on left side by i/o, 6-pin)
    "Header 2 - pin 3": {'name': 'button_1', 'type': 'Button', 'pin': 12},  # Jim Hawkins, header 2, pin 3
    "Header 2 - pin 4": {'name': 'button_2', 'type': 'Button', 'pin': 16},  # Jim Hawkins, header 2, pin 4
    "Header 2 - pin 5": {'name': 'button_3', 'type': 'Button', 'pin': 20},   # Jim Hawkins, header 2, pin 5
    "Header 2 - pin 6": {'name': 'input4', 'type': 'Button', 'pin': 21}, # Jim Hawkins, JUMPERED TO header 1, pin 8
    
}


    ##################################
    #### 3.0 UI, Buttons, Display ####
    ##################################

#### (3.1) # LCD setup
# 'I2C/16x2', 'I2C/20x4', 'wired/16x2', None
LCD_TYPE = 'I2C/20x4'
I2C_LCD_ADDRESS = 0x27
I2C_COM_DELAY = .0001    # this fixes the OSError: Remote I/O error that some LCDs get.  Good displays are .0001
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
BUTTON_PULLUP = False

BUTTON_BOUNCE = .1  # debounce time for buttons.  0 to .3 seconds.  Limit switches are best at .1

# button hold time is used for time it takes to hold a button for a function
BUTTON_HOLD_TIME = 2


    #############################
    #### 4.0 Life Test Timer ####
    #############################

# input names
input1_name = 'lower limit switch'
input2_name = 'upper limit switch'

# output names
output1_name = 'motor up'
output2_name = 'motor down'

timer_dict = {
    'timer1': {'name': 'lower limit switch',
        'countdown': 0,
        'status': False,
        'timer_time_sec': 25,
        },
    }




