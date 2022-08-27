#!/usr/bin/env python
'''
file name:  Modem_Rider_goop.py
date created:
created by:
project/support:                # root or script it supports
description:

special instruction:
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'

from dataclasses import dataclass

@dataclass
class Goop():
    ''' data
    '''
    ### Internet Monitor
    internet_good: bool = False
    modem_cycle_monitor = {
        'off count': 15,
        'modem count': 15,
        'WIFI count': 15,
        'cycling': False,
        }

    modem_cycle_monitor_DEFAULTS = {
        'off count': 15,
        'modem count': 15,
        'WIFI count': 15,
        'cycling': False,
        }

    min_Good_Internet: int = 0
    min_No_Internet: int = 0
    day_min_Good_Internet: int = 0
    day_min_No_Internet: int = 0

    #### general voyager2 parameters ####
    startup_seconds = 15 # must be greater than 10 seconds
    flash_flag: bool = True

    button1: bool = False
    button2: bool = False
    button3: bool = False

    # ### buttons args
    ''' used for passing arguements to button functions in UI
    '''
    button1_args = {}
    button2_args = {}
    button3_args = {}

    # ### Screens
    current_screen_group = 'home'
    current_screen = 'main'

    ''' init_UI flag
    if True, then will init UI.  Typically this includes new button functions
    '''
    init_UI = False 


    