#!/usr/bin/env python
'''
file name:  NN_main.py
date created:  August 27, 2022
created by:
project/support: NomiNomiV2       # root or script it supports
description:  initial tests for timing loop, runs on MacPro

special instruction:
    Voyager2 files:
    1. XX_main.py # DO NOT PUT STATE PARAMETERS AND FLAGS HERE!
    2. v2_gpio.py # contains all gpio and sensor objects
    3. XX_goop.py # contains all parameters indluding sensor readings and state flags
    4. XX_UI.py # all button functions contained here, note how functions are passed. 
        Button parameters are kept in Goop and then called by button function, not passed.
    configuration and timing loop
    Should not contain any class objects (e.g. sensors, etc.)
 
    goop contains data (Goop) and is only instantiated in main

rev 0.0.1 initial DEV
rev 0.0.2 updated to new button and UI functionality.
rev 0.0.3 ready to put in sailboat
rev 0.0.4 NomiNomi2 Sailboat DEV
'''
__project_name__ = "NomiNomi2"
__revision__ = 'v0.0.4'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'


# standard imports
from time import time

# voyager2 imports
from v2_gpio import Machine
import RPi_utilities as RPi_util
from v2_LCD_utility import LCD_manager

# #### Application-Specific Imports ####
import config
from NN_goop import Goop
import NN_UI as UI

# import sensors
from sensors.gps_utility import Ultimate_GPS
from sensors.compass_utility import Compass
from sensors.heel_utility import ADXL345
from sensors.wind_vane_utility import Wind_Vane

# instantiate key objects
machine = Machine()

# goop is instantiated here and then placed in other modules if needed
goop = Goop()
UI.goop = goop  # put goop into UI

lcd_mgr = LCD_manager()

# sensor objects
gps = Ultimate_GPS()
compass = Compass()
heel_sensor = ADXL345()
wind_vane = Wind_Vane()

# #### timing parameters
last_milli = 0
start_milli = time() * 1000

# get current time and set for "last"
if config.use_hwclock is True:
    # XXX> add hwclock read here
    pass
else:
    # use Internet clock
    (last_hour, last_minute, last_second) = RPi_util.get_time(config.local_time_zone)

# #### Initialize UI
# LCD welcome display (will stay on for goop.startup_seconds)
_menu_dict = UI.UI_dict['welcome'].get('screen')
_menu_dict['line2'] = f'{__project_name__}'
_menu_dict['line3'] = f'rev: {__revision__}'
IP_address = RPi_util.get_IP_address()
_menu_dict['line4'] = f'{IP_address}'
lcd_mgr.display_menu(_menu_dict)

# initialize key parameters
goop.init_UI = True  # requires init at end of startup
goop.button1_args['machine'] = machine  # this allows next screen to modify buttons
goop.button1_args['lcd'] = lcd_mgr  # this allows UI to print to lcd


while True and goop.main_thread_inhibit is False:
    milli = (time() * 1000) - start_milli
    
    # ### deal with millis rolling
    # this should never happen
    if milli < 0:
        milli = (time() * 1000)
        last_milli = 0

    if (milli - last_milli) >= config.POLL_MILLIS:
        # get current time
        if config.use_hwclock is True:
            # XXX> add hwclock read here
            pass
        else:
            # use Internet clock
            HHMMSS = RPi_util.get_time(config.local_time_zone)

        # ### Jobs that run every poll
        # XXX> call GPS update (this must be called at least twice as fast as GPS update
        # which is set at 1 second)

        # ### Second ####
        if last_second != HHMMSS[2]:
            # redo last_second
            last_second = HHMMSS[2]
            #### Every second jobs ####
            print(f'\n{HHMMSS}')
            print(f'goop.init_UI: {goop.init_UI}')

            # ### always actions (startup and regular)
            if goop.sailing is True:
                # #### Sailing every second actions ####

                # #### GPS read ####
                # XXX> read_GPS here
                pass

                # #### Sensors Read ####



            # #####################################
            # #### Startup and Regular Actions ####
            # #####################################

            if goop.startup_seconds > 1 and goop.startup_seconds != 10:
                # #### Startup Actions Only ####
                goop.startup_seconds -= 1
            elif goop.startup_seconds == 10:
                '''performs a screen change at 10 seconds'''
                goop.startup_seconds -= 1

            else:
                # #### Regular Actions (after startup) ####
                # ### Change button functions once
                if goop.init_UI is True:
                    print('\nNN_main, after startup init buttons')
                    machine.redefine_button_actions(
                        button1_function = UI.next_screen,
                        button2_function = UI.UI_dict[goop.current_screen_group][goop.current_screen].get('button2'),
                        button3_function = UI.UI_dict[goop.current_screen_group][goop.current_screen].get('button3')
                        )
                    goop.init_UI = False

                # ### update LCD
                lcd_mgr.display_menu(UI.UI_dict[goop.current_screen_group][goop.current_screen].get('screen'))


            


            # ----------------------------------------------

            #### On second jobs ####
            if int(HHMMSS[2]) % 5 == 0 or int(HHMMSS[2]) == 0:
                ### every 5 second jobs ####
                print('run 5 second job')
                # ----------------------------------------------

            if int(HHMMSS[2]) % 15 == 0 or int(HHMMSS[2]) == 0:
                ### every 15 second jobs ####
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
    
