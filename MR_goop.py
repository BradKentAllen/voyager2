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
    flash_flag: bool = True

    button1: bool = False
    button2: bool = False
    button3: bool = False

    # ### buttons args
    button1_args = [None]
    button2_args = [None]
    button3_args = [None]



    