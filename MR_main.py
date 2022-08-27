#!/usr/bin/env python
'''
file name:  MR_main.py
date created:  July 10, 2022
created by:
project/support: voyager2       # root or script it supports
description:  initial tests for timing loop, runs on MacPro

special instruction:
    Voyager2 files:
    1. MR_main.py # DO NOT PUT STATE PARAMETERS AND FLAGS HERE!
    2. v2_gpio.py # contains all gpio and sensor objects
    3. MR_goop.py # contains all parameters indluding sensor readings and state flags
    4. MR_buttons.py # all button functions contained here, note how functions are passed. 
        Button parameters are kept in Goop and then called by button function, not passed.
    configuration and timing loop
    Should not contain any class objects (e.g. sensors, etc.)
    brain contains gpio, sensors, LCD manager, etc.
    goop contains data (Goop)

rev 0.0.1 initial DEV
rev 0.0.2 updated to new button and UI functionality.
rev 0.0.3 ready to put in sailboat
'''
__project_name__ = "Modem Runner"
__revision__ = 'v0.0.3'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'


# standard imports
from time import time

# voyager2 imports
from v2_gpio import Machine
import RPi_utilities as RPi_util
from v2_LCD_utility import LCD_manager
from sensors.check_internet import check_URL

# #### Application-Specific Imports ####
import config
from MR_goop import Goop
import MR_UI as UI

# instantiate key objects
machine = Machine()

# goop is instantiated here and then placed in other modules if needed
goop = Goop()
UI.goop = goop  # put goop into UI

lcd_mgr = LCD_manager()

last_milli = 0
start_milli = time() * 1000
(last_hour, last_minute, last_second) = RPi_util.get_time(config.local_time_zone)

# #### Initialize UI
# LCD welcome display (will stay on for goop.startup_seconds)
_menu_dict = UI.UI_dict['welcome'].get('screen')
_menu_dict['line1'] = f'{__project_name__}'
_menu_dict['line2'] = f'rev: {__revision__}'
lcd_mgr.display_menu(_menu_dict)

# initialize key parameters
goop.init_UI = True  # requires init at end of startup
goop.button1_args['machine'] = machine  # this allows next screen to modify buttons
goop.button1_args['lcd'] = lcd_mgr  # this allows UI to print to lcd


while True and goop.main_thread_inhibit is False:
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
            # print(f'\n{HHMMSS}')

            # ### always actions (startup and regular)
            ''' XXX test flash LED's
            if goop.flash_flag is True:
                machine.LED("blue_LED_1", "ON")
                machine.LED("blue_LED_2", "OFF")
                machine.LED("yellow_LED", "OFF")
                machine.LED("red_LED", "ON")
                goop.flash_flag = False
            else:
                machine.LED("blue_LED_1", "OFF")
                machine.LED("blue_LED_2", "ON")
                machine.LED("yellow_LED", "ON")
                machine.LED("red_LED", "OFF")
                
                goop.flash_flag = True
            '''

            # ### cycle modem and WIFI
            # IMPORANT: check Internet is called in 15 sec functions
            if goop.modem_cycle_monitor.get('cycling') is True:
                machine.LED("cycling_LED", "ON")
                # XXXX add cycling logic here
            else:
                machine.LED("cycling_LED", "OFF")

            # #####################################
            # #### Startup and Regular Actions ####
            # #####################################

            if goop.startup_seconds > 1 and goop.startup_seconds != 10:
                # #### Startup Actions Only ####
                goop.startup_seconds -= 1
            elif goop.startup_seconds == 10:
                '''performs a screen change at 10 seconds'''
                _menu_dict = UI.UI_dict['welcome'].get('screen')
                IP_address = RPi_util.get_IP_address()
                _menu_dict['line2'] = f'{IP_address}'
                lcd_mgr.display_menu(_menu_dict)
                goop.startup_seconds -= 1

            else:
                # #### Regular Actions (after startup) ####
                # ### Change button functions once
                if goop.init_UI is True:
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

                # ### check internet
                # IMPORTANT: more logic and cycling LED are in 1 second functions
                goop.internet_good = check_URL(config.check_URL2, config.URL_timeout)

                if goop.internet_good is True:
                    machine.LED("Internet_Bad_LED", "OFF")
                    machine.LED("Internet_Good_LED", "ON")

                    # #### turn off cycling
                    goop.modem_cycle_monitor = goop.modem_cycle_monitor_DEFAULTS

                else:
                    machine.LED("Internet_Bad_LED", "ON")
                    machine.LED("Internet_Good_LED", "OFF")

                    # ### start cycling modem and WIFI
                    # this is the only place this occurs
                    goop.modem_cycle_monitor['cycling'] = True



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
    
