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
__project_name__ = "Life Tester A"
__revision__ = 'v1.5'
__status__ = 'beta' # 'DEV', 'alpha', 'beta', 'production'


    ################################
    ####   (0.0) Test Process   ####
    ################################

'''
Each stage as the following parameters:
stage name: this can be any unique name

action:  "go UP", "go DOWN", "stop"
msg: up to 20 characters that appear on LCD
timer:  0 (do not modify)
trigger time:  integer (will trigger on time), "up limit switch", "down limit switch"
    If trigger time is set to 0, then the action will occur immediately
trigger action:  what occurs at trigger time or trigger action
    "next action", "log cycles", "log timer", "log timer and cycles", fault" (log will log and go to next action)
log name:  column data goes in on the log.  This is assigned to a goop parameter which is then used for the log.
    If trigger action is "fault", log name is the fault message
count cycle:  True or False, if True will record 1 cycle at end of stage

'''

TEST_PROCESS_DICT = {
    "1 up cycle": {
        "action": "go UP",
        "message": "up cycle",
        "timer": 0,
        "trigger time": "up limit switch",
        "trigger action": "log timer",
        
        "log name": None,
        "count cycle": False,
        },
    "2 top delay": {
        "action": "stop",
        "message": "up delay, 15 secs",
        "timer": 0,
        "trigger time": 15,
        "trigger action": "next action",
        
        "log name": None,
        "count cycle": False,
        },
    "3 down cycle": {
        "action": "go DOWN",
        "message": "down cycle",
        "timer": 0,
        "trigger time": "down limit switch",
        "trigger action": "next action",
        
        "log name": None,
        "count cycle": False,
        },
    "4 down delay": {
        "action": "stop",
        "message": "down delay, 15 secs",
        "timer": 0,
        "trigger time": 15,
        "trigger action": "log cycles",
        
        "log name": None,
        "count cycle": False,
        },
        
    }




    ################################
    #### (1.0) General Settings ####
    ################################

# #### (1.0) Test Settings
CAN_PASS_UP_SWITCH = False
CAN_PASS_DOWN_SWITCH = False

# #### (1.1) File structure
DATA_DIR = "data"
LIFE_CYCLES_FILENAME = "life_cycles"
LOG_FILENAME = "log"

LOG_COLUMNS = ('date', 'cycles', 'session cycles', 'up time', 'motor temp', 'ambient temp')

LOG_DEGREES_F = True # False will log in C

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










