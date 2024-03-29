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
    2. WS_goop.py # contains all parameters indluding sensor readings and state flags
    3. v2_gpio.py # contains all gpio.  All gpio should be called rom within the Machine 
    object created by the import from v2_gio.  Failure to do so will result in thread
    conflicts.  Buttons use interrupts which are created in v2_gio.  If additional
    interrupts are required, they are initiated from main (here)
    3. LCD manager is important for driving the LCD.  Make sure you only end up with
    one LCD_manager or the display will have all sorts of problems.
    4. WS_UI.py # all button functions are contained here, note how functions are passed.
    If a button function requires parameters, those button parameters are kept in Goop 
    and then called by button function, not passed.
    
    5. I2C sensors are initiated and called from main.  If they are required elsewhere,
    pass the sensor object to the function from main.

copyright 2022, MIT License, AditNW LLC

rev 1.0 DEV
'''

# standard imports
import time
import signal
import pickle

# standard  voyager2 imports
from v2_gpio import Machine
import RPi_utilities as RPi_util
from v2_LCD_utility import LCD_manager

# #### Application-Specific Imports ####
# These may require modification
import config
from WS_goop import Goop
import WS_UI as UI
import WS_utilities as util

# other specialized utilities
import API.tide_text as tides

# sensors
import sensors.bmp280 as bmp280
import sensors.HIH6121 as HIH6121


global keyboard_stop_flag  # used to bypass fault handler in keyboard interrupt
keyboard_stop_flag = False


class voyager_runner():
    def __init__(self):
        # #### instantiate key objects
        # first the key voyager objects
        # these will only be instantiated in main
        self.machine = Machine()
        self.goop = Goop()
        self.lcd_mgr = LCD_manager()

        # Assign the key objects to the voyager utilities
        # IMPORTANT:  this prevents multiple instantiations of goop, machine,
        # and lcd_mgr
        UI.goop = self.goop  # put goop into UI
        UI.machine = self.machine  # put machine into UI
        UI.lcd_mgr = self.lcd_mgr

        util.goop = self.goop

        # #### Check for Persistent Data
        # # set rain_day if restarting
        try:
            with open('persist_data.pkl', 'rb') as file:
                persist_data = pickle.load(file)
        except FileNotFoundError:
            pass
        else:
            if isinstance(persist_data, dict):
                # #### retreive and use persist data
                if persist_data.get('date') == time.strftime('%d', time.localtime()):
                    self.goop.rain_day = persist_data.get('rain_day', self.goop.rain_day)
                    self.goop.barometric_string = persist_data.get('barometric_string', self.goop.barometric_string)



        # #### initialize I2C sensors
        self.bmp280 = bmp280.BMP280()
        self.HIH6121 = HIH6121.HIH6121sensor()

        # #### Initialize UI
        # LCD welcome display (will stay on for goop.startup_seconds)
        _menu_dict = UI.return_UI_dict()['welcome'].get('screen')
        self.lcd_mgr.display_menu(_menu_dict)
        
        # #### File Management
        
        # #### initialize key parameters
        self.goop.init_UI = True  # requires init at end of startup

        self.goop.barometric_last = int(self.bmp280.get_pressure(in_Hg=True) * 100)

        # get tide data and save as pickle file
        util.update_tides_with_API()
        retreived_tide_dict = util.get_pickled_cache('tide_dict')

        self.goop.tide_data_dict = tides.tide_LCD(
            tide_dict=retreived_tide_dict,
            previous_tide_data=None,
            tide_max=15.7,
            tide_min=-4,
            display_range=20,
            )

        # ### Assign functions to interupts
        # Buttons 1, 2, and 3 are assigned dynamically but other "buttons", which
        # includes limit switches, are assinged here
        # example:  self.machine.gpio_objects.get('up_switch').when_pressed = UI.up_limit_switch_on_contact
        self.machine.gpio_objects.get('rain_gage').when_pressed = UI.rain_gage_contact



    def run(self):
        # initiate key timing variables and update time
        last_milli = 0
        start_milli = time.time() * 1000
        (last_hour, last_minute, last_second) = RPi_util.get_time(config.local_time_zone)



        # #####################
        # #### Timing Loop ####
        # #####################
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
                # Jobs here will run with every poll.  This can be as fast as polling
                # but may be less often if processing time consumes a poll time



                # ----------------------------------------------


                #### Second ####

                if last_second != HHMMSS[2]:
                    # update last_second
                    last_second = HHMMSS[2]
                    #### Every second jobs ####
                    # print(f'\n{HHMMSS}')

                    # ### always actions (startup and regular)
                    # LED indicators
                    if self.goop.flash_flag is True:
                        if self.goop.fault is False:
                            # normal pulse
                            if config.flash_green_pulse is True:
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

                    if self.goop.startup_seconds > 1:
                        # #### Startup Actions Only ####
                        self.goop.startup_seconds -= 1
                    elif self.goop.startup_seconds in (1, 2):
                        # allows intermediate display
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
                        try:
                            self.lcd_mgr.display_menu(screen_dict)
                        except OSError:
                            # this may occur due to an I2C issue with other boards.
                            # restart is to get rid of bad graphics on LCD
                            self.lcd_mgr.restart_LCD()

                        # ### fancy tide display
                        # Will overlay a custom tide display if appropriate menu
                        if self.goop.current_screen_group == 'weather':
                            if self.goop.current_screen in (1,):
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
                                    self.lcd_mgr.display_char(character, 4, count)


                    


                    # ----------------------------------------------

                    #### On second jobs ####

                    self.goop.screen_message = f'seconds: {int(time.time()) % 100}'





                    if int(HHMMSS[2]) % 5 == 0 or int(HHMMSS[2]) == 0:
                        ### every 5 second jobs ####
                        pass

                        # ----------------------------------------------

                    if int(HHMMSS[2]) % 15 == 0 or int(HHMMSS[2]) == 0:
                        # update sensor data
                        try:
                            self.goop.temp_in = self.bmp280.get_temp(F=True)
                            self.goop.pressure = self.bmp280.get_pressure(in_Hg=True)
                        except OSError:
                            self.goop.temp_in = 99
                            self.goop.pressure = 99
                            print(f'OSError in BMP280')

                        # rain gage count
                        self.goop.rain_hour = self.goop.rain_count * config.rain_gage_per_count

                        # Get outside temp and RH
                        self.goop.RH, temp_C, self.goop.temp_out = self.HIH6121.returnTempRH()  # error trap in sensor returns 1, 99, 99

                        dew_point_C = temp_C - ((100 - self.goop.RH)/5)
                        self.goop.dew_point = (dew_point_C * 1.8) + 32

                        # change display
                        if self.goop.current_screen_group == "weather":
                            self.goop.current_screen += 1
                            if self.goop.current_screen > len(UI.return_UI_dict()[self.goop.current_screen_group]):
                                self.goop.current_screen = 1
                            self.goop.init_UI = True


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
                            
                            self.goop.tide_data_dict = tides.tide_LCD(
                                tide_dict=retreived_tide_dict,
                                previous_tide_data=previous_tide_data,
                                tide_max=15.7,
                                tide_min=-4,
                                display_range=20,
                                )



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

                            # rain gage
                            self.goop.rain_day +=self.goop.rain_hour
                            self.goop.rain_hour = 0
                            self.goop.rain_count = 0

                            # barometric pressure trend
                            _current_barometric = int(self.goop.pressure * 100)
                            print(f'current: {_current_barometric}, last: {self.goop.barometric_last}, test delta: {config.barometric_hundredth_test}')
                            if (_current_barometric - self.goop.barometric_last) > 2 * config.barometric_hundredth_test:
                                _graphic = '+'
                                self.goop.barometric_last = int(self.bmp280.get_pressure(in_Hg=True) * 100)
                            elif (_current_barometric - self.goop.barometric_last) > config.barometric_hundredth_test:
                                _graphic = '^'
                                self.goop.barometric_last = int(self.bmp280.get_pressure(in_Hg=True) * 100)
                            elif (_current_barometric - self.goop.barometric_last) < -2 * config.barometric_hundredth_test:
                                _graphic = 'L'
                                self.goop.barometric_last = int(self.bmp280.get_pressure(in_Hg=True) * 100)
                            elif (_current_barometric - self.goop.barometric_last) < -1 * config.barometric_hundredth_test:
                                _graphic = 'v'
                                self.goop.barometric_last = int(self.bmp280.get_pressure(in_Hg=True) * 100)
                            else:
                                _graphic = '-'

                            self.goop.barometric_string = self.goop.barometric_string[1:] + _graphic

                            # #### Persist Data
                            # this can be performed at any time
                            persist_data = {
                                'date': time.strftime('%d', time.localtime()),
                                'rain_day': self.goop.rain_day,
                                'barometric_string': self.goop.barometric_string,
                            }

                            with open('persist_data.pkl', 'wb') as file:
                                pickle.dump(persist_data, file)


                            # Midnight actions
                            if int(HHMMSS[0]) == 0:
                                # clear rain for day
                                self.goop.rain_day = 0
                            # ----------------------------------------------
                            

                #### polling marker
                last_milli = milli

            

            #### update milli
            milli = (time.time() * 1000) - start_milli



# ###############################################
# #### Fault Handlers and Keyboard Interrupt ####
# ###############################################

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
        # ### DEBUG MODE
        # in Debug there are no fail safes to make sure gpio is OFF
        # in case of an error.  Be careful running from here.
        print('!!! WARNING:  Running in DEBUG mode')
        app.run()
    else:
        # ### Normal run with fault handlers
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


 













        
