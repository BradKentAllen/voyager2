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

# goop is filled by XXX_main
goop = None


    #########################
    #### Button Function ####
    #########################

def start():
    print('START Life Tester')

def manual_up():
    print('manual up')

def manual_down():
    print('manual down')

def stop_all():
    print('stop all')


def test3_with_args():
    print('MR_buttons: test3_with_args')
    try:
        print(f'the returned arg is: {goop.button3_args[0]}')
    except IndexError:
        print('IndexError in buttons test3_with args')


def shutdown_RPi():
    goop.main_thread_inhibit = True
    goop.button1_args['lcd'].display_clear()
    goop.button1_args['lcd'].display_multi_line(
        message_list = [('will shut down', 'left'),]
        )
    time.sleep(5)
    RPi_util.shutdown_RPi()


def reboot_RPi():
    print('>>>> reboot RPi in UI')
    goop.main_thread_inhibit = True
    goop.button1_args['lcd'].display_clear()
    goop.button1_args['lcd'].display_multi_line(
        message_list = [('will reboot', 'left'),]
        )
    time.sleep(5)
    print('start reboot')
    RPi_util.reboot_RPi()



    ###################################
    #### User Interface Dictionary ####
    ###################################

''' Buttons pass function from above.

'''


UI_dict = {
    'welcome': {
        'screen': {
            'line1': 'Welcome',
            'line1_justification': 'left',
            'line2': 'to Voyager',
            'line2_justification': 'left',
            'line3': f'rev {config.__revision__}',
            'line3_justification': 'left',
            'line4': 'line 4',
            'line4_justification': 'left',
            },
        'button2': None,
        'button3': None,
        },
    'home': {
        'main': {
            'screen': {
                'line1': 'ready to start',
                'line1_justification': 'left',
                'line2': 'line 2',
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
                'line1': 'Manual Operation',
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
                'line1': 'Manual Operation',
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
        
        'MX': {
            'screen': {
                'line1': 'RPi OFF',
                'line1_justification': 'left',
                'line2': 'shut down RPi >',
                'line2_justification': 'right',
                'line3': 'reboot RPi >',
                'line3_justification': 'right',
                'line4': '<next',
                'line4_justification': 'left',
                },
            'button2': reboot_RPi,
            'button3': shutdown_RPi,
            }
        },
    'run': {
        'running': {
            'screen': {
                'line1': 'RUNNING',
                'line1_justification': 'left',
                'line2': 'line 2',
                'line2_justification': 'left',
                'line3': f'{RPi_util.get_IP_address()}',
                'line3_justification': 'left',
                'line4': '<next         STOP>',
                'line4_justification': 'left',
                },
            'button2': start,
            'button3': test3_with_args,
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

    










