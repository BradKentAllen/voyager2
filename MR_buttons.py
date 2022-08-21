#!/usr/bin/env python
'''
file name:  MR_buttons.py
date created:  August 21, 2022
created by:
project/support: voyager2       # root or script it supports
description:  
    MR_buttons has all buttons functions
    Button functions are passed to the GPIO, so they can not have arguements
    To pass paramaters to a bettun, set in Goop, then use with the functions

special instruction:
    All buttons functions must be here
    Button functions are passed to v2_gpio for action

rev 0.0.1 initial DEV
rev 0.0.2 updating with buttons for use with sailboat
'''

import config
from MR_goop import Goop as goop


def next_screen():
    '''changes to next screen
    '''
    next_screen_flag = False
    first_screen_group = None
    new_screen = None

    # work through all screens in the current screen group
    for count, _screen in enumerate(config.display_dict.get(goop.current_screen_group)):
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


def test():
    print('MR_buttons test only')


def test3_with_args():
    print('MR_buttons: test3_with_args')
    try:
        print(f'the returned arg is: {goop.button3_args[0]}')
    except IndexError:
        print('IndexError in buttons test3_with args')