#!/usr/bin/env python
# -*- coding: utf-8 -*-
# config.py for NomiNomi
#!/usr/bin/env python
'''
file name: config.py
date created: August 27, 2022
created by: Brad Allen
project/support: NomiNomi (voyager2) # root or script it supports
description:

special instruction:
'''
__revision__ = 'v0.0.4'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'


    ################################
    #### (1.0) General Settings ####
    ################################

#### (1.2) # Time Zone
local_time_zone = 'US/Pacific'

use_hwclock = False # will use hardware clock instead of Internet time

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
    'pulse_LED': 14,

    # these are customizable
    # availabe types:  'LED', 'Output'

        # Header 1 (by power jack, 6-pin) ONLY 4-PIN on Modem Rider
    'i_o_5': {'name': 'button_3', 'type': 'Button', 'pin': 5},
    'i_o_6': {'name': 'button_2', 'type': 'Button', 'pin': 6},
    'i_o_13': {'name': 'button_1', 'type': 'Button', 'pin': 13},
    
}


    ##################################
    #### 3.0 UI, Buttons, Display ####
    ##################################

#### (3.1) # LCD setup
# 'I2C/16x2', 'I2C/20x4', 'wired/16x2', None
LCD_TYPE = 'I2C/20x4'
I2C_LCD_ADDRESS = 0x23
BACKLIGHT_OFF_TIME = 3  # minutes until backlight goes off

custom_chars = {
    'GPS': 0,
    'down arrow': 3,
    'water drop': 1,
    'up arrow': 2,
    }












