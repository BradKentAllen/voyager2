#!/usr/bin/env python
'''
file name:  Modem_Rider_main.py
date created:  July 10, 2022
created by:
project/support: voyager2       # root or script it supports
description:  initial tests for timing loop, runs on MacPro

special instruction:
    Voyager2 files:
    1. MR_main.py # DO NOT PUT STATE PARAMETERS AND FLAGS HERE!
    2. v2_gpio.py # contains all gpio and sensor objects
    3. MR_goop.py # contains all parameters
    configuration and timing loop
    Should not contain any class objects (e.g. sensors, etc.)
    brain contains gpio, sensors, LCD manager, etc.
    goop contains data (Goop)
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'


# standard imports
from time import time

# voyager2 imports
from v2_gpio import Machine
import RPi_utilities as RPi_util
from v2_LCD_utility import LCD_manager

# #### Application-Specific Imports ####
import config
from MR_goop import Goop

# instantiate key objects
machine = Machine()
goop = Goop()
lcd_mgr = LCD_manager()

last_milli = 0
start_milli = time() * 1000
(last_hour, last_minute, last_second) = RPi_util.get_time(config.local_time_zone)

# LCD welcome display
lcd_mgr.display_menu(config.display_dict['welcome'].get('screen'))


while True:
    milli = (time() * 1000) - start_milli
    
    #### deal with millis rolling
    # this should never happen
    if milli < 0:
        milli = (time() * 1000)
        last_milli = 0


    if (milli - last_milli) >= config.POLL_MILLIS:
        HHMMSS = RPi_util.get_time(config.local_time_zone)

        #### Jobs that run every poll
        # none

        #### Second ####
        if last_second != HHMMSS[2]:
            # redo last_second
            last_second = HHMMSS[2]
            #### Every second jobs ####
            print(f'\n{HHMMSS}')
            if goop.flash_flag is True:
                machine.LED("blue_LED_1", "ON")
                machine.LED("blue_LED_2", "OFF")
                machine.LED("yellow_LED", "OFF")
                machine.LED("red_LED", "ON")
                machine.LED("working_LED", "ON")
                machine.LED("Internet_Bad_LED", "OFF")
                machine.LED("Internet_Good_LED", "ON")
                goop.flash_flag = False
            else:
                machine.LED("blue_LED_1", "OFF")
                machine.LED("blue_LED_2", "ON")
                machine.LED("yellow_LED", "ON")
                machine.LED("red_LED", "OFF")
                machine.LED("working_LED", "OFF")
                machine.LED("Internet_Bad_LED", "ON")
                machine.LED("Internet_Good_LED", "OFF")
                goop.flash_flag = True


            # ----------------------------------------------

            #### On second jobs ####
            if int(HHMMSS[2])%5 == 0 or int(HHMMSS[2]) == 0:
                ### every 5 second jobs ####
                print('run 5 second job')
                # ----------------------------------------------

            if int(HHMMSS[2])%15 == 0 or int(HHMMSS[2]) == 0:
                ### every 5 second jobs ####
                print('run 15 second job')
                # ----------------------------------------------


            #### Minute ####
            if last_minute != HHMMSS[1]:
                last_minute = HHMMSS[1]
                #### Every minute jobs ####
                pass
                # ----------------------------------------------
                

                #### On minute jobs ####
                if int(HHMMSS[1])%5 == 0 or int(HHMMSS[1]) == 0:
                    #### Every 5 minute jobs ####
                    pass
                    # ----------------------------------------------

                if int(HHMMSS[1])%15 == 0 or int(HHMMSS[1]) == 0:
                    #### Every 15 minute jobs ####
                    pass
                    # ----------------------------------------------

                if int(HHMMSS[1])%30 == 0 or int(HHMMSS[1]) == 0:
                    #### Every 30 minute jobs ####
                    pass
                    # ----------------------------------------------

                #### Hour ####
                if last_hour != HHMMSS[0]:
                    last_hour = HHMMSS[0]
                    #### Every hour jobs ####
                    pass
                    # ----------------------------------------------
                    

        #### polling marker
        last_milli = milli

    

    #### update milli
    milli = (time() * 1000) - start_milli
    
