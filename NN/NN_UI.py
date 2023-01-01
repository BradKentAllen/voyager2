#!/usr/bin/env python
'''
file name:  NN_buttons.py
date created:  August 27, 2022
created by:
project/support: NomiNomi2       # root or script it supports
description:  
    XX_buttons has all buttons functions
    Button functions are passed to the GPIO, so they can not have arguements
    To pass paramaters to a bettun, set in Goop, then use with the functions

special instruction:
    All buttons functions must be here
    Button functions are passed to v2_gpio for action

rev 0.0.1 initial DEV
rev 0.0.2 updating with buttons for use with sailboat
'''

import time

# standard voyager imports
import RPi_utilities as RPi_util

# goop is filled by XXX_main
goop = None


# ########################
# ### Button Function ####
# ########################

def test_button2():
    print('Button 2 pressed')


def test_button3():
    print('Button 3 pressed')


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
            'line2': 'line 2',
            'line2_justification': 'left',
            'line3': 'line 3',
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
                'line1': 'home screen',
                'line1_justification': 'left',
                'line2': 'line 2',
                'line2_justification': 'right',
                },
            'button2': test_button2,
            'button3': test_button3,
            },
        'MX': {
            'screen': {
                'line1': 'shut down RPi >',
                'line1_justification': 'right',
                'line2': 'reboot RPi >',
                'line2_justification': 'right',
                },
            'button2': reboot_RPi,
            'button3': shutdown_RPi,
            }
        }     
    }


    ###############################
    #### Button 1 - Next Screen####
    ###############################
    # IMPORTANT:  this must be after the UI_dict

def next_screen():
    '''changes to next screen
    '''
    print('\n>>>> run UI.next_screen')
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

        # test for current screen
        if _screen == goop.current_screen:
            next_screen_flag = True

    # this happens if on the last screen in the screen_group
    if new_screen is None:
        new_screen = first_screen_group

    # update the new screen
    goop.current_screen  = new_screen
    goop.init_UI = True # will run full init of UI

    










