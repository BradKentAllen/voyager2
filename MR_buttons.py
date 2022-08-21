#!/usr/bin/env python
'''
file name:  MR_buttons.py
date created:  August 21, 2022
created by:
project/support: voyager2       # root or script it supports
description:  
    MR_buttons has all buttons functions
    button functions are passed to the GPIO, so they can not have parameters
    Paramaters are set in Goop, then used by the functions

special instruction:
    All buttons functions must be here
    Button functions are passed to v2_gpio for action

rev 0.0.1 initial DEV
rev 0.0.2 updating with buttons for use with sailboat
'''

from MR_goop import Goop as goop


def next_screen():
    '''changes to next screen
    '''
    print('change to next screen')


def test():
    print('MR_buttons test only')


def test3_with_args():
    print('MR_buttons: test3_with_args')
    try:
        print(f'the returned arg is: {goop.button3_args[0]}')
    except IndexError:
        print('IndexError in buttons test3_with args')