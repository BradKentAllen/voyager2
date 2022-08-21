#!/usr/bin/env python
'''
file name:  MR_buttons.py
date created:  August 21, 2022
created by:
project/support: voyager2       # root or script it supports
description:  initial tests for timing loop, runs on MacPro

special instruction:
    All buttons functions must be here
    Button functions are passed to v2_gpio for action

rev 0.0.1 initial DEV
rev 0.0.2 updating with buttons for use with sailboat
'''


def next_screen():
    '''changes to next screen
    '''
    print('change to next screen')

def test():
    print('MR_buttons test only')

def test__with_arg(button_number=0):
    print(f'MR_buttons:  NEW FUNC for button {button_number}')