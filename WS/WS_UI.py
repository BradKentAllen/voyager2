#!/usr/bin/env python
'''
file name:  WS_UI.py
date created:  October 4, 2022
created by:  Brad Allen, AditNW LLC
project/support: Weather Station (voyager)      # root or script it supports
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
import datetime

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
    pass

@fault_decorator
def stop():
    pass

@fault_decorator
def stop_all():
    pass
    '''
    machine.output("UP_relay", "OFF")
    machine.output("DOWN_relay", "OFF")
    goop.mx = False
    '''

@fault_decorator
def rain_gage_contact():
    print('rain gage contact')
    goop.rain_count +=1

# #### Tests
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


def return_next_tide():
    if goop.tide_data_dict is None:
        return 'no data'

    _time_now = datetime.datetime.strftime(datetime.datetime.now(), '%-I:%M')
    _tide_height = goop.tide_data_dict.get('tide height', 99)
    _next_tide = goop.tide_data_dict.get('next tide', 'n')
    _next_tide_height = goop.tide_data_dict.get('next tide height', 99)
    _next_tide_time = datetime.datetime.strftime(goop.tide_data_dict.get('next tide time'), '%-I:%M')

    if _next_tide == 'H':
        _next_tide = 'High'
    elif _next_tide == 'L':
        _next_tide = "Low"
    else:
        _next_tide = "error"

    return f"{_next_tide} at {_next_tide_time}"


def return_current_tide():
    if goop.tide_data_dict is None:
        return 'no data'

    _time_now = datetime.datetime.strftime(datetime.datetime.now(), '%-I:%M')
    _tide_height = goop.tide_data_dict.get('tide height', 99)
    _next_tide = goop.tide_data_dict.get('next tide', 'n')
    _next_tide_height = goop.tide_data_dict.get('next tide height', 99)
    _next_tide_time = datetime.datetime.strftime(goop.tide_data_dict.get('next tide time'), '%I:%M')

    return f"{_tide_height:.1f} > {_next_tide_height:.1f}"


def return_tide_string():
    try:
        return f"{goop.tide_data_dict.get('display string')}"
    except AttributeError:
        return "no tide data"







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
                'line1': f'{RPi_util.get_IP_address()}',
                'line1_justification': 'left',
                'line2': f'rev {config.__revision__}, {config.__status__}',
                'line2_justification': 'left',
                'line3': None,
                'line3_justification': None,
                'line4': None,
                'line4_justification': None,
                },
            'button2': None,
            'button3': None,
            },
        'home': {
            'main': {
                'screen': {
                    'line1': f"{return_tide_string()}",
                    'line1_justification': 'left',
                    'line2': f"{return_next_tide()} ",
                    'line2_justification': 'left',
                    'line3': None,
                    'line3_justification': None,
                    'line4': None,
                    'line4_justification': None,
                    },
                'button2': start,
                'button3': None,
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
        'weather': {
            1: { # Tide
                'screen': {
                    'line1': None,  # filled in main based on screen number
                    'line1_justification': 'left',
                    'line2': f"{return_next_tide()} ",
                    'line2_justification': 'left',
                    'line3': f"{return_current_tide()} ",
                    'line3_justification': 'left',
                    'line4': f"{datetime.datetime.strftime(datetime.datetime.now(), '%-I:%M')} in: {goop.temp_in:.0f}  out: {goop.temp_out:.0f}",
                    'line4_justification': 'left',
                    },
                'button2': None,
                'button3': None,
                },
            2: { # Conditions
                'screen': {
                    'line1': f"{goop.temp_out:.0f}, RH {goop.RH:.0f}% DP {goop.dew_point:.0f}",  # filled in main based on screen number
                    'line1_justification': 'left',
                    'line2': f"{goop.pressure:.1f}\" Hg",
                    'line2_justification': 'left',
                    'line3': f"rain {goop.rain_hour:.2f}\" {(goop.rain_day + goop.rain_hour):.2f}\"",
                    'line3_justification': 'left',
                    'line4': f"{datetime.datetime.strftime(datetime.datetime.now(), '%-I:%M')}",
                    'line4_justification': 'left',
                    },
                'button2': None,
                'button3': None,
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

    










