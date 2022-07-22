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
    flash_flag: bool = True
    RH: int = 0
    temp: float = 0.0

    RH_max: int = 0
    RH_min: int = 100
    Temp_max: int = 0
    Temp_min: int = 100

    min_Good_Internet: int = 0
    min_No_Internet: int = 0
    day_min_Good_Internet: int = 0
    day_min_No_Internet: int = 0

    #### general voyager2 parameters ####
    lcd_line1: str = "Welcome"
    lcd_line2: str = "to TV Cabinet"

    button1: bool = False
    button2: bool = False
    button3: bool = False



    