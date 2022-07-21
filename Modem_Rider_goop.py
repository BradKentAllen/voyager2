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


#### Define the GPIO for the board
# Each GPIO function must be defined here
# The pin numbers can be over-ridden by the config file (this allows a common
# machine module to support different machines with different pinouts but to
# use the same logic)
# IMPORTANT:  PIN #'s are BCM, not board.  There is no provision for using 
# board numbering in RPi_Voyager

## Format for pins varies slightly by function
# LED: [function, pin#, 'LED', False]
# Button: [None, pin#, 'button', False] name and pin# matter only
# Servo: [None, pin#, 'servo', 0] - last value is initial position (-1 to 1)
gpio_func = {
    'pulse LED': [None, 22, 'LED', False],
    'button1' : [None, 17, 'button', False],
    'button2' : [None, 27, 'button', False],
    'relay modem': [None, 23, 'output', False],
    'relay wifi': [None, 24, 'output', False],
    'Internet good': [None, 16, 'LED', False],
    'no Internet': [None, 20, 'LED', False],

}

@dataclass
class Goop():
    ''' data
    '''
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



    