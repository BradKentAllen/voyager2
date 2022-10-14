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
    Main loop handler is in main
    '''
    # XXXX - Change to show on LCD
    stop_all()
    goop.fault = True
    print(f'\nTHREAD FAULT: {type(e).__name__}')
    print(f'reason: {e.args}')
    goop.mx = False
    goop.running = False
    goop.current_screen_group = "home"
    goop.current_screen = "main"
    goop.init_UI = True # will run full init of UI
    
    exit()

def fault_decorator(func):
    def wrapper():
        try:
            func()
        except Exception as e:
            fault_handler(e)
    return wrapper

    #########################
    #### Button Function ####
    #########################

@fault_decorator
def start():
    goop.mx = False
    goop.running = True
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

@fault_decorator
def up_limit_switch_on_contact():
    print('CONTACT up limit switch')
    if machine.gpio_objects.get('UP_relay').value == 1:
        stop_all()

@fault_decorator
def up_limit_switch_on_release():
    print('RELEASE up limit switch')

@fault_decorator
def down_limit_switch_on_contact():
    print('>>CONTACT down limit switch<<')
    if machine.gpio_objects.get('DOWN_relay').value == 1:
        stop_all()


def test3_with_args():
    print('MR_buttons: test3_with_args')
    try:
        print(f'the returned arg is: {goop.button3_args[0]}')
    except IndexError:
        print('IndexError in buttons test3_with args')

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
    stop_all()
    time.sleep(5)
    goop.main_thread_inhibit = True
    lcd_mgr.display_clear()
    lcd_mgr.display_multi_line(
        message_list = [('will shut down', 'left'),]
        )
    time.sleep(15)
    RPi_util.shutdown_RPi()
    

@fault_decorator
def reboot_RPi():
    print('>>>> reboot RPi in UI')
    stop_all()
    time.sleep(5)
    goop.main_thread_inhibit = True
    lcd_mgr.display_clear()
    lcd_mgr.display_multi_line(
        message_list = [('will reboot', 'left'),]
        )
    time.sleep(15)
    print('start reboot')
    RPi_util.reboot_RPi()


# #### User interface information retrieval
# these are required because goop is not available when UI is instantiated
def get_life_cycles():
    try:
        return goop.life_cycles
    except AttributeError:
        return 0

def get_message():
    try:
        return goop.screen_message
    except AttributeError:
        return "all is good today"


    ###################################
    #### User Interface Dictionary ####
    ###################################

''' Buttons pass function from above.

'''


UI_dict = {
    'welcome': {
        'screen': {
            'line1': 'Loading...',
            'line1_justification': 'left',
            'line2': 'Voyager 2',
            'line2_justification': 'left',
            'line3': f'rev {config.__revision__}',
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
                'line1': f'{get_message()}',
                'line1_justification': 'left',
                'line2': f'life: {get_life_cycles()}',
                'line2_justification': 'left',
                'line3': f'{RPi_util.get_IP_address()}',
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
                'line2': f'life: {get_life_cycles()}',
                'line2_justification': 'left',
                'line3': f'{RPi_util.get_IP_address()}',
                'line3_justification': 'left',
                'line4': '              STOP>',
                'line4_justification': 'left',
                },
            'button2': stop,
            'button3': None,
            },

        },     
    }


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
    for count, _screen in enumerate(UI_dict.get(goop.current_screen_group)):
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
    goop.init_UI = True # will run full init of UI

    










