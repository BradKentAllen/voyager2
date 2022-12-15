#!/usr/bin/env python
'''
file name:  seal_main.py
date created:  November 30, 2022
created by:  Brad Allen, AditNW LLC
project/support: Seal       # root or script it supports
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

rev 1.0 converted from DD
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
from VT_goop import Goop
import VT_UI as UI
import VT_utilities as util



global keyboard_stop_flag  # used to bypass fault handler in keyboard interrupt
keyboard_stop_flag = False


class voyager_runner():
    def __init__(self):
        # instantiate key objects
        self.machine = Machine()
        self.goop = Goop()
        self.lcd_mgr = LCD_manager()

        #self.bmp280 = bmp280.BMP280()

        # make objects availabe in UI for customized methods
        UI.goop = self.goop  # put goop into UI
        UI.machine = self.machine  # put machine into UI
        UI.lcd_mgr = self.lcd_mgr

        util.goop = self.goop

        # #### Initialize UI
        # LCD welcome display (will stay on for goop.startup_seconds)
        _menu_dict = UI.return_UI_dict()['welcome'].get('screen')
        self.lcd_mgr.display_menu(_menu_dict)

        # #### Initiate I2C sensors
        
        # #### File Management
        
        # #### initialize key parameters
        self.goop.init_UI = True  # requires init at end of startup


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
                    #print(f'\n{HHMMSS}')

                    

                    # ### always actions (startup and regular)
                    # XXX test flash LED's
                    if self.goop.flash_flag is True:
                        #print('ON')
                        if self.goop.fault is False:
                            # normal pulse
                            self.machine.LED("green_LED", "ON")
                            self.machine.LED("blue_LED_1", "ON")
                            self.machine.LED("blue_LED_2", "ON")
                            
                            self.machine.LED("red_LED", "ON")
                            
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
                    else:
                        # #### Regular Actions (after startup) ####
                        # ### Change button functions once
                        if self.goop.init_UI is True:
                            print('\n### redefine buttons')
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
                        self.lcd_mgr.display_menu(screen_dict)


                    


                    # ----------------------------------------------

                    #### On second jobs ####

                    self.goop.screen_message = f'seconds: {int(time.time()) % 100}'





                    if int(HHMMSS[2]) % 5 == 0 or int(HHMMSS[2]) == 0:
                        ### every 5 second jobs ####
                        pass
                        # ----------------------------------------------

                    if int(HHMMSS[2]) % 15 == 0 or int(HHMMSS[2]) == 0:
                        # update sensor data
                        #self.goop.temp_in = self.bmp280.get_temp(F=True)
                        #self.goop.pressure = self.bmp280.get_pressure(in_Hg=True)
                        pass


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


 













        
