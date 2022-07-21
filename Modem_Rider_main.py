#!/usr/bin/env python
'''
file name:  Modem_Rider_main.py
date created:  July 10, 2022
created by:
project/support: voyager2       # root or script it supports
description:  initial tests for timing loop, runs on MacPro

special instruction:
    Voyager2 files:
    1. Modem_Rider_main.py
    2. 
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
import RPi_utilities as RPi_util

# #### Application-Specific Imports ####
import Modem_Rider_config as config
from Modem_Rider_brain import Brain
from Modem_Rider_goop import Goop, gpio_func



last_milli = 0
start_milli = time() * 1000
(last_hour, last_minute, last_second) = RPi_util.get_time(config.local_time_zone)


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
        print(HHMMSS)

        #### Second ####
        if last_second != HHMMSS[2]:
            # redo last_second
            last_second = HHMMSS[2]
            #### Every second jobs ####
            print('***')


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
    
