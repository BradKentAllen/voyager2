#!/usr/bin/env python
'''
file name:  WS_main.py
date created:  November 19, 2022
created by:  Brad Allen, AditNW LLC
project/support: Weather Station (voyager)      # root or script it supports
description:  main timing featues for Life Tester

special instruction:
    Voyager2 files:
    1. WS_main.py # DO NOT PUT STATE PARAMETERS AND FLAGS HERE!
    2. v2_gpio.py # contains all gpio and sensor objects
    3. WS_goop.py # contains all parameters indluding sensor readings and state flags
    4. WS_UI.py # all button functions contained here, note how functions are passed. 
        Button parameters are kept in Goop and then called by button function, not passed.
    configuration and timing loop
    Should not contain any class objects (e.g. sensors, etc.)

copyright 2022, MIT License, AditNW LLC

rev 1.0 DEV
'''

# standard imports
import time
import signal

# voyager2 imports
from v2_gpio import Machine
import RPi_utilities as RPi_util
from v2_LCD_utility import LCD_manager

# #### Application-Specific Imports ####
import config
from WS_goop import Goop
import WS_UI as UI
import WS_utilities as util

import API.tide_text as tides
import sensors.bmp280 as bmp280
#import sensors.TH02_RH_temp as TH02_RH
import sensors.HIH6121 as HIH6121


global keyboard_stop_flag  # used to bypass fault handler in keyboard interrupt
keyboard_stop_flag = False


class voyager_runner():
    def __init__(self):
        # instantiate key objects
        self.machine = Machine()
        self.goop = Goop()
        self.lcd_mgr = LCD_manager()

        # initialize sensors
        self.bmp280 = bmp280.BMP280()
        #self.th02 = TH02_RH.TH02()
        self.HIH6121 = HIH6121.HIH6121sensor()

        # make objects availabe in UI for customized methods
        UI.goop = self.goop  # put goop into UI
        UI.machine = self.machine  # put machine into UI
        UI.lcd_mgr = self.lcd_mgr

        util.goop = self.goop

        # #### Initialize UI
        # LCD welcome display (will stay on for goop.startup_seconds)
        _menu_dict = UI.return_UI_dict()['welcome'].get('screen')
        self.lcd_mgr.display_menu(_menu_dict)
        
        # #### File Management
        
        # #### initialize key parameters
        self.goop.init_UI = True  # requires init at end of startup

        # get tide data and save as pickle file
        util.update_tides_with_API()
        retreived_tide_dict = util.get_pickled_cache('tide_dict')

        self.goop.tide_data_dict = tides.tide_LCD(retreived_tide_dict)

        # ### Assign functions to interupts
        # Buttons 1, 2, and 3 are assigned dynamically but other "buttons", which
        # includes limit switches, are assinged here
        # example:  self.machine.gpio_objects.get('up_switch').when_pressed = UI.up_limit_switch_on_contact



    def run(self):
        # initiate key timing variables and update time
        last_milli = 0
        start_milli = time.time() * 1000
        (last_hour, last_minute, last_second) = RPi_util.get_time(config.local_time_zone)

        while True and self.goop.main_thread_inhibit is False:
            milli = (time.time() * 1000) - start_milli
            
            #### deal with millis rolling
            # this should never happen
            if milli < 0:
                milli = (time.time() * 1000)
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
                    if self.goop.flash_flag is True:
                        #print('ON')
                        if self.goop.fault is False:
                            # normal pulse
                            self.machine.LED("green_LED", "ON")
                        else:
                            # pulse in a fault
                            self.machine.LED("red_LED", "ON")

                        self.goop.flash_flag = False
                    else:
                        # green pulse
                        self.machine.LED("green_LED", "OFF")

                        self.machine.LED("blue_LED_1", "OFF")
                        self.machine.LED("blue_LED_2", "OFF")
                        
                        self.machine.LED("red_LED", "OFF")

                        #machine.output("UP_relay", "OFF")
                        #machine.output("DOWN_relay", "ON")
                        
                        self.goop.flash_flag = True



                    # #####################################
                    # #### Startup and Regular Actions ####
                    # #####################################

                    '''
                    if self.goop.startup_seconds > 1 and self.goop.startup_seconds != 5:
                        # #### Startup Actions Only ####
                        self.goop.startup_seconds -= 1
                    elif self.goop.startup_seconds == 5:
                        #performs a screen change at 10 seconds
                        _menu_dict = UI.return_UI_dict()['welcome'].get('screen')
                        IP_address = RPi_util.get_IP_address()
                        _menu_dict['line2'] = f'{IP_address}'
                        self.lcd_mgr.display_menu(_menu_dict)
                        self.goop.startup_seconds -= 1

                    elif self.goop.startup_seconds == 1:
                        self.goop.screen_message = "Ready to Run"
                        self.goop.startup_seconds -= 1
                    '''

                    if self.goop.startup_seconds > 1:
                        # #### Startup Actions Only ####
                        self.goop.startup_seconds -= 1
                    elif self.goop.startup_seconds in (1, 2):
                        self.goop.current_screen_group = "weather"
                        self.goop.current_screen = 1
                        self.goop.init_UI = True
                        self.goop.startup_seconds -= 1
                    else:
                        # #### Regular Actions (after startup) ####
                        # ### Change button functions once
                        if self.goop.init_UI is True:
                            self.machine.redefine_button_actions(
                                button1_function = UI.next_screen,
                                button2_function = UI.return_UI_dict()[self.goop.current_screen_group][self.goop.current_screen].get('button2'),
                                button3_function = UI.return_UI_dict()[self.goop.current_screen_group][self.goop.current_screen].get('button3')
                                )
                            self.goop.init_UI = False

                        screen_dict = UI.return_UI_dict()[self.goop.current_screen_group][self.goop.current_screen].get('screen')

                        if self.goop.fault is True:
                            if config.DEBUG is True: print('>>>> FAULT DISPLAY <<<<')
                            # lead with fault during operation
                            screen_dict['line1'] = 'FAULT stop'
                            #screen_dict['line4'] = self.goop.fault_msg

                        # ### update LCD
                        # DEBUG XXXXXX
                        try:
                            self.lcd_mgr.display_menu(screen_dict)
                        except OSError:
                            # this appears to accur do to an I2C issue with other boards.
                            # restart is to get rid of bad graphics on LCD
                            print(f'OS error in LCD second, restart LCD')
                            print(f'{screen_dict}\n')
                            self.lcd_mgr.restart_LCD()

                        # ### fancy tide display
                        # Will overlay a custom tide display if appropriate menu
                        if self.goop.current_screen_group == 'weather':
                            if self.goop.current_screen in (1, 2):
                                # overlay fancy tide
                                for count, character in enumerate(UI.return_tide_string()):
                                    character = ord(character)
                                    if character == 43:
                                        # above zero water level
                                        character = config.custom_chars.get('wave1')
                                    elif character == 45:
                                        # below zero water level
                                        character = config.custom_chars.get('wave2')
                                    elif character == 60:
                                        # person walking left, to low
                                        character = config.custom_chars.get('person1')
                                    elif character == 62:
                                        # person walking right, to high
                                        character = config.custom_chars.get('person2')
                                    elif character == 48:
                                        # zero tide marker
                                        character = config.custom_chars.get('buoy')
                                    self.lcd_mgr.display_char(character, 1, count)


                    


                    # ----------------------------------------------

                    #### On second jobs ####

                    self.goop.screen_message = f'seconds: {int(time.time()) % 100}'





                    if int(HHMMSS[2]) % 5 == 0 or int(HHMMSS[2]) == 0:
                        ### every 5 second jobs ####
                        if self.goop.current_screen_group == "weather":
                            self.goop.current_screen += 1
                            if self.goop.current_screen > len(UI.return_UI_dict()[self.goop.current_screen_group]):
                                self.goop.current_screen = 1
                            self.goop.init_UI = True

                        # ----------------------------------------------

                    if int(HHMMSS[2]) % 15 == 0 or int(HHMMSS[2]) == 0:
                        # update sensor data
                        self.goop.temp_in = self.bmp280.get_temp(F=True)
                        self.goop.pressure = self.bmp280.get_pressure(in_Hg=True)

                        # Get outside temp and RH
                        #temp_C, self.goop.temp_out, self.goop.RH = self.th02.get_temp_RH()
                        self.goop.RH, temp_C, self.goop.temp_out = self.HIH6121.returnTempRH()

                        dew_point_C = temp_C - ((100 - self.goop.RH)/5)
                        self.goop.dew_point = (dew_point_C * 1.8) + 32


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
                            # update tide display data
                            retreived_tide_dict = util.get_pickled_cache('tide_dict')

                            # previous tide data is used after midnight until next tide change
                            previous_tide_data = self.goop.tide_data_dict.get('previous tide data')
                            
                            self.goop.tide_data_dict = tides.tide_LCD(retreived_tide_dict, previous_tide_data)

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
                            # update tide information
                            util.update_tides_with_API()
                            # ----------------------------------------------
                            

                #### polling marker
                last_milli = milli

            

            #### update milli
            milli = (time.time() * 1000) - start_milli


def fault_handler(e):
    '''Handles faults within the timing loops
    Faults in gpio threads are handled by the decorator in UI
    '''
    global keyboard_stop_flag
    UI.stop_all()

    if keyboard_stop_flag is False:
        UI.LED_lights(
            blue1="OFF",
            blue2='OFF',
            green='OFF',
            red='ON')
        if isinstance(e, str):
            pass
        else:
            print(f'reason: {e.args}')
    else:
        # this should only occur in keyboard interrupt
        pass
    exit()

def keyboardInterruptHandler(signal, frame):
    '''safe handle ctl-c stop'''
    global keyboard_stop_flag
    keyboard_stop_flag = True
    UI.stop_all()
    UI.LED_lights(
        blue1="ON",
        blue2='ON',
        green='OFF',
        red='OFF')
    exit()


if __name__ == "__main__":
    app = voyager_runner()

    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    if config.DEBUG is True:
        print('!!! WARNING:  Running in DEBUG mode')
        app.run()
    else:
        try:
            app.run()
        except Exception as e:
            fault_handler(e)
        except:
            fault_handler('unspecified fault')
        else:
            UI.stop_all()
            print('nothing was caught, this is else')
            exit()


 













        
