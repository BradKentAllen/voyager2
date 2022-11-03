#!/usr/bin/env python
'''
file name:  LTA_UI.py
date created:  October 4, 2022
created by:  Brad Allen, AditNW LLC
project/support: Life Tester A      # root or script it supports
description:  
    Has all buttons functions
    Button functions are passed to the GPIO, so they can not have arguements
    To pass paramaters to a bettun, set in Goop, then use with the functions

special instruction:
    All buttons functions must be here
    Button functions are passed to v2_gpio for action

    IMPORTANT:  Button functions are threads.  This can cause a number of issues including 
    including with LCD functions and os functions.

copyright 2022, MIT License, AditNW LLC

rev 1.0 initial creation from MR_UI.py

'''

import time

# standard voyager imports
import RPi_utilities as RPi_util

# application specific imports
import config

# key objects filled by XXX_main.py
goop = None
machine = None
lcd_mgr = None


def fault_handler(e):
    '''Decorator fault handler for threads
    Can also be called individually

    IMPORTANT:  the overall Main loop handler is in main
    '''
    goop.fault = True
    
    if isinstance(e, str):
        if config.DEBUG is True:
            print('\nCalled Fault')
            print(e)
        goop.fault_msg = e
    else:
        if config.DEBUG is True:
            print(f'\nTHREAD FAULT: {type(e).__name__}')
            print(f'reason: {e.args}')
        goop.fault_msg = e
    goop.mx = False
    goop.running = False
    goop.current_screen_group = "home"
    goop.current_screen = "main"
    goop.init_UI = True # will run full init of UI


def fault_decorator(func):
    def wrapper():
        try:
            func()
        except Exception as e:
            fault_handler(e)
    return wrapper

    ############################
    #### GPIO Utility Calls ####
    ############################

def LED_lights(blue1, blue2, green, red):
    machine.LED("blue_LED_1", blue1)
    machine.LED("blue_LED_2", blue2)
    machine.LED("green_LED", green)
    machine.LED("red_LED", red)


    #########################
    #### Button Function ####
    #########################

@fault_decorator
def start():
    goop.mx = False
    goop.running = True
    # XXXX change to down for initial direction
    goop.position = "down"
    goop.current_screen_group = "run"
    goop.current_screen = "running"
    goop.init_UI = True # will run full init of UI

@fault_decorator
def stop():
    stop_all()
    goop.mx = False
    goop.running = False
    goop.current_screen_group = "home"
    goop.current_screen = "main"
    goop.screen_message = "PAUSED"
    goop.init_UI = True # will run full init of UI

@fault_decorator
def stop_all():
    machine.output("UP_relay", "OFF")
    machine.output("DOWN_relay", "OFF")
    goop.mx = False

@fault_decorator
def manual_up():
    goop.mx = True
    machine.output("UP_relay", "ON")

@fault_decorator
def manual_down():
    goop.mx = True
    machine.output("DOWN_relay", "ON")

# #### Limit switches

@fault_decorator
def up_limit_switch_on_contact():
    print('\n>>>CONTACT up limit switch')
    if machine.gpio_objects.get('UP_relay').value == 1:
        if config.CAN_PASS_UP_SWITCH is False:
            stop_all()

@fault_decorator
def up_limit_switch_on_release():
    print('RELEASE up limit switch')

@fault_decorator
def down_limit_switch_on_contact():
    print('>>CONTACT down limit switch<<')
    if machine.gpio_objects.get('DOWN_relay').value == 1:
        if config.CAN_PASS_DOWN_SWITCH is False:
            stop_all()


def test3_with_args():
    print('MR_buttons: test3_with_args')
    try:
        print(f'the returned arg is: {goop.button3_args[0]}')
    except IndexError:
        print('IndexError in buttons test3_with args')


# ### OS functions

@fault_decorator
def os():
    ''' returns to home screen
    '''
    stop_all()
    goop.mx = False
    goop.running = False
    goop.current_screen_group = "os"
    goop.current_screen = "reboot"
    goop.init_UI = True # will run full init of UI

@fault_decorator
def cancel():
    ''' returns to home screen
    '''
    stop_all()
    goop.mx = False
    goop.running = False
    goop.current_screen_group = "home"
    goop.current_screen = "main"
    goop.init_UI = True # will run full init of UI

@fault_decorator
def shutdown_RPi():
    print('>>>> shut down RPi in UI')
    stop_all()
    goop.mx = True
    goop.os_operation = 'shut down'
    

@fault_decorator
def reboot_RPi():
    print('>>>> reboot RPi in UI')
    stop_all()
    goop.mx = True
    goop.os_operation = 'reboot'


    #########################
    #### UI Dict Methods ####
    #########################

def return_message():
    try:
        return goop.screen_message
    except AttributeError:
        return "no message"

def return_life_cycles():
    try:
        return str(goop.life_cycles)
    except AttributeError:
        return "X"

def return_session_cycles():
    try:
        return str(goop.session_cycles)
    except AttributeError:
        return "X"

def return_temps():
    try:
        return f'{goop.motor_temp:.0f} / {goop.ambient_temp:.0f}'
    except AttributeError:
        return "X"

    #########################
    #### Screen Updates ####
    #########################
    # screen updates modify a portion of the LCD
    # this avoids flashing the LCD to change a monitored parameter such as time

def update_current_timer():
    try:
        _time = str(goop.current_timer)
    except AttributeError:
        _time =  "X"

    lcd_mgr.update_with_string(_time.rjust(4, ' '), 1, 16)




    ###################################
    #### User Interface Dictionary ####
    ###################################

''' Buttons pass function from above.

'''

def return_UI_dict():
    _UI_dict = {
        'welcome': {
            'screen': {
                'line1': f'{config.__project_name__}',
                'line1_justification': 'left',
                'line2': 'Voyager 2',
                'line2_justification': 'left',
                'line3': f'rev {config.__revision__}, {config.__status__}',
                'line3_justification': 'left',
                'line4': '',
                'line4_justification': 'left',
                },
            'button2': None,
            'button3': None,
            },
        'home': {
            'main': {
                'screen': {
                    'line1': f'{return_message()}',
                    'line1_justification': 'left',
                    'line2': f'total cycles: {return_life_cycles()}',
                    'line2_justification': 'left',
                    'line3': f'IP: {RPi_util.get_IP_address()}',
                    'line3_justification': 'left',
                    'line4': '<next         START>',
                    'line4_justification': 'left',
                    },
                'button2': start,
                'button3': None,
                },

            'manual up': {
                'screen': {
                    'line1': 'Manual Up',
                    'line1_justification': 'left',
                    'line2': 'manual UP >',
                    'line2_justification': 'right',
                    'line3': 'STOP >',
                    'line3_justification': 'right',
                    'line4': '<next',
                    'line4_justification': 'left',
                    },
                'button2': stop_all,
                'button3': manual_up,
                },

            'manual down': {
                'screen': {
                    'line1': 'Manual Down',
                    'line1_justification': 'left',
                    'line2': 'STOP >',
                    'line2_justification': 'right',
                    'line3': 'manual DOWN >',
                    'line3_justification': 'right',
                    'line4': '<next',
                    'line4_justification': 'left',
                    },
                'button2': manual_down,
                'button3': stop_all,
                },
            'settings': {
                'screen': {
                    'line1': 'Settings',
                    'line1_justification': 'left',
                    'line2': 'OS >',
                    'line2_justification': 'right',
                    'line3': 'Future >',
                    'line3_justification': 'right',
                    'line4': '<next',
                    'line4_justification': 'left',
                    },
                'button2': None,
                'button3': os,
                },
            },
        'os': {
            'reboot': {
                'screen': {
                    'line1': 'Reboot RPi',
                    'line1_justification': 'left',
                    'line2': 'Reboot NOW >',
                    'line2_justification': 'right',
                    'line3': 'cancel>',
                    'line3_justification': 'right',
                    'line4': '<next',
                    'line4_justification': 'left',
                    },
                'button2': cancel,
                'button3': reboot_RPi,
                },
            'shut down': {
                'screen': {
                    'line1': 'Shut Down RPi',
                    'line1_justification': 'left',
                    'line2': 'Shut Down NOW >',
                    'line2_justification': 'right',
                    'line3': 'cancel>',
                    'line3_justification': 'right',
                    'line4': '<next',
                    'line4_justification': 'left',
                    },
                'button2': cancel,
                'button3': shutdown_RPi,
                },
            },
        'run': {
            'running': {
                'screen': {
                    'line1': 'RUNNING',
                    'line1_justification': 'left',
                    'line2': f'{return_message()}',
                    'line2_justification': 'left',
                    'line3': f'cycles: {return_session_cycles()} / {return_life_cycles()}',
                    'line3_justification': 'left',
                    'line4': f'{return_temps():<9}     STOP>',
                    'line4_justification': 'left',
                    },
                'button2': stop,
                'button3': None,
                },

            },     
        }
    return _UI_dict


    ###############################
    #### Button 1 - Next Screen####
    ###############################
    # IMPORTANT:  this must be after the UI_dict

def next_screen():
    '''changes to next screen
    '''
    #print('\n>>>> run UI.next_screen')
    #print(UI_dict.get(goop.current_screen_group))

    next_screen_flag = False
    first_screen_group = None
    new_screen = None

    # work through all screens in the current screen group
    for count, _screen in enumerate(return_UI_dict().get(goop.current_screen_group)):
        # save the first screen, for use if on the last screen
        if count == 0:
            first_screen_group = _screen

        # retain new screen (this has to be before the test)
        if next_screen_flag is True:
            new_screen = _screen
            break

        # test for current screen
        if _screen == goop.current_screen:
            next_screen_flag = True

    # this happens if on the last screen in the screen_group
    if new_screen is None:
        new_screen = first_screen_group

    #print(f'new_screen: {new_screen}')

    # update the new screen
    goop.current_screen  = new_screen
    goop.mx = False
    goop.init_UI = True # will run full init of UI

    










