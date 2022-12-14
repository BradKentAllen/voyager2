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
rev 1.1 move to class format for debug and except-safe
rev 1.2 rewrite run logic to test_process_dict
rev 1.3 refine
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
from LTA_goop import Goop
import LTA_UI as UI
import LTA_utilities as util

from sensors.ads1115driver import ADS1115

global keyboard_stop_flag  # used to bypass fault handler in keyboard interrupt
keyboard_stop_flag = False

class voyager_runner():
    def __init__(self):
        # instantiate key objects
        self.machine = Machine()
        self.goop = Goop()
        self.lcd_mgr = LCD_manager()

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
        self.ads = ADS1115()

        # #### File Management
        util.validate_data_dir()
        util.validate_log_file()


        self.goop.life_cycles = util.get_life_cycles()

        # #### initialize key parameters
        self.goop.init_UI = True  # requires init at end of startup

        _status = util.find_initial_position(
            up_limit_switch=self.machine.gpio_objects.get('up_switch').is_pressed,
            down_limit_switch=self.machine.gpio_objects.get('down_switch').is_pressed,
            )

        # instantiate copy of test process dict (config parameters should not be modified)
        self.goop.test_process = config.TEST_PROCESS_DICT.copy()

        self.goop.test_stage = util.determine_initial_stage()


        # ### Assign functions to interupts
        # Buttons 1, 2, and 3 are assigned dynamically but other "buttons", which
        # includes limit switches, are assinged here
        self.machine.gpio_objects.get('up_switch').when_pressed = UI.up_limit_switch_on_contact
        self.machine.gpio_objects.get('up_switch').when_released = UI.up_limit_switch_on_release
        self.machine.gpio_objects.get('down_switch').when_pressed = UI.down_limit_switch_on_contact

        self.goop.screen_message = "Ready after startup"


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
                            screen_dict['line4'] = self.goop.fault_msg

                        # ### update LCD
                        # try/except added Dec 6, 2022 based on tests with weather station
                        try:
                            self.lcd_mgr.display_menu(screen_dict)
                        except OSError:
                            self.lcd_mgr.restart_LCD()


                    


                    # ----------------------------------------------

                    #### On second jobs ####
                    
                    if self.goop.running is True:
                        
                        # ####################
                        # #### RUN LOGIC #####
                        # ####################
                        _update_UI_flag, _action = util.run_logic(
                            up_limit_switch=self.machine.gpio_objects.get('up_switch').is_pressed,
                            down_limit_switch=self.machine.gpio_objects.get('down_switch').is_pressed,
                            )

                        if _update_UI_flag == "fault":
                            UI.fault_handler(_action)

                        if config.DEBUG is True: print(f'## action: {_action}')

                        # execute gpio actions
                        if _action == "go UP":
                            self.machine.output("UP_relay", "ON")
                        elif _action == "go DOWN":
                            self.machine.output("DOWN_relay", "ON")
                        elif _action == "stop":
                            self.machine.output("UP_relay", "OFF")
                            self.machine.output("DOWN_relay", "OFF")

                        # display timer
                        UI.update_current_timer()


                        # ####################

                    elif self.goop.mx is True:
                        # MX covers manual operations, when nothing happens here,
                        # and os operations
                        if self.goop.os_operation == 'reboot':
                            print('start reboot')
                            self.lcd_mgr.display_multi_line(
                                message_list = [('will Reboot', 'left'),
                                    ('NOW', 'left'),
                                    ('', 'left'),
                                    ('Wait for Restart', 'left')]
                                )
                            time.sleep(10)
                            self.lcd_mgr.display_clear()
                            time.sleep(2)

                            RPi_util.reboot_RPi()

                        elif self.goop.os_operation == 'shut down':
                            print('start shut down')
                            self.lcd_mgr.display_multi_line(
                                message_list = [('will shut down', 'left'),
                                ('NOW', 'left'),
                                ('', 'left'),
                                ('wait for full off', 'left')]
                                )
                            time.sleep(10)
                            self.lcd_mgr.display_clear()
                            time.sleep(2)

                            RPi_util.shutdown_RPi()

                    else:
                        UI.stop_all()






                    if int(HHMMSS[2]) % 5 == 0 or int(HHMMSS[2]) == 0:
                        ### every 5 second jobs ####
                        #print('run 5 second job')
                        pass

                        # ----------------------------------------------

                    if int(HHMMSS[2]) % 15 == 0 or int(HHMMSS[2]) == 0:
                        ### every 15 second jobs ####
                        #print('run 15 second job')
                        # read motor temps
                        # Error traps if ADS1115 is not attached
                        try:
                            mv_A0 = self.ads.readADCSingleEnded(0)
                            mv_A1 = self.ads.readADCSingleEnded(1)

                            self.goop.ambient_temp = util.return_TMP36_temp(mv_A0, f_degrees=config.LOG_DEGREES_F)
                            self.goop.motor_temp = util.return_TMP36_temp(mv_A1, f_degrees=config.LOG_DEGREES_F)
                        except OSError:
                            self.goop.ambient_temp = 999
                            self.goop.motor_temp = 999







                        # ----------------------------------------------


                    #### Minute ####
                    if last_minute != HHMMSS[1]:
                        last_minute = HHMMSS[1]
                        #### Every minute jobs ####
                        # record life cycles to permanent disk file
                        util.save_life_cycles(self.goop.life_cycles)

                        # write key parameters to log
                        util.write_one_log_line()
                    
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
            util.write_fault_log_line(e)
        else:
            print(f'reason: {e.args}')
            util.write_fault_log_line(e.args)
    else:
        # this should only occur in keyboard interrupt
        pass
    exit()

def keyboardInterruptHandler(signal, frame):
    '''safe handle ctl-c stop'''
    global keyboard_stop_flag
    util.write_fault_log_line("keyboard interrupt")
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


 













        
