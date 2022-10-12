#!/usr/bin/env python
'''
file name:  LTA_main.py
date created:  October 4, 2022
created by:  Brad Allen, AditNW LLC
project/support: Life Tester A       # root or script it supports
description:  main timing featues for Life Tester

special instruction:
    Voyager2 files:
    1. LTA_main.py # DO NOT PUT STATE PARAMETERS AND FLAGS HERE!
    2. v2_gpio.py # contains all gpio and sensor objects
    3. LTA_goop.py # contains all parameters indluding sensor readings and state flags
    4. LTA_UI.py # all button functions contained here, note how functions are passed. 
        Button parameters are kept in Goop and then called by button function, not passed.
    configuration and timing loop
    Should not contain any class objects (e.g. sensors, etc.)

copyright 2022, MIT License, AditNW LLC

rev 1.0 initial creation from MR_main.py
'''

# standard imports
from time import time

# voyager2 imports
from v2_gpio import Machine
import RPi_utilities as RPi_util
from v2_LCD_utility import LCD_manager

# #### Application-Specific Imports ####
import config
from LTA_goop import Goop
import LTA_UI as UI
import LTA_utilities as util

# instantiate key objects
machine = Machine()
goop = Goop()
lcd_mgr = LCD_manager()

# make objects availabe in UI for customized methods
UI.goop = goop  # put goop into UI
UI.machine = machine  # put machine into UI
UI.lcd_mgr = lcd_mgr

# initiate key timing variables and update time
last_milli = 0
start_milli = time() * 1000
(last_hour, last_minute, last_second) = RPi_util.get_time(config.local_time_zone)

# #### Initialize UI
# LCD welcome display (will stay on for goop.startup_seconds)
_menu_dict = UI.UI_dict['welcome'].get('screen')
_menu_dict['line1'] = f'{config.__project_name__}'
_menu_dict['line2'] = f'rev: {config.__revision__}'
lcd_mgr.display_menu(_menu_dict)

# #### File Management
util.validate_data_dir()
goop.life_cycles = util.get_life_cycles()

# initialize key parameters
goop.init_UI = True  # requires init at end of startup

# ### Assign functions to interupts
# Buttons 1, 2, and 3 are assigned dynamically but other "buttons", which
# includes limit switches, are assinged here
machine.gpio_objects.get('up_switch').when_pressed = UI.up_limit_switch_on_contact
machine.gpio_objects.get('up_switch').when_released = UI.up_limit_switch_on_release
machine.gpio_objects.get('down_switch').when_pressed = UI.down_limit_switch_function


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
            # XXX test flash LED's
            if goop.flash_flag is True:
                #print('ON')

                machine.LED("blue_LED_1", "ON")
                #machine.LED("blue_LED_2", "OFF")
                #machine.LED("yellow_LED", "OFF")
                #machine.LED("red_LED", "ON")

                #machine.output("UP_relay", "ON")
                #machine.output("DOWN_relay", "OFF")

                goop.flash_flag = False
            else:
                #print("OFF")

                machine.LED("blue_LED_1", "OFF")
                #machine.LED("blue_LED_2", "ON")
                #machine.LED("yellow_LED", "ON")
                #machine.LED("red_LED", "OFF")

                #machine.output("UP_relay", "OFF")
                #machine.output("DOWN_relay", "ON")
                
                goop.flash_flag = True



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
                #print(f'>>>DEBUG {goop.current_screen_group} - {goop.current_screen}')
                lcd_mgr.display_menu(UI.UI_dict[goop.current_screen_group][goop.current_screen].get('screen'))


            


            # ----------------------------------------------

            #### On second jobs ####
            if int(HHMMSS[2]) % 5 == 0 or int(HHMMSS[2]) == 0:
                ### every 5 second jobs ####
                print('run 5 second job')
                if machine.gpio_objects.get('up_switch').is_pressed is True:
                    print('>>>up switch engaged')
                else:
                    print('>>>up switch open')
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
    
