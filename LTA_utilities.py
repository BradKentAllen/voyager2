#!/usr/bin/env python
'''
file name:  LTA_utilities.py
date created:  October 12, 2022
created by:  Brad Allen, AditNW LLC
project/support: Life Tester A       # root or script it supports
description:  utitilities for import into LTA_main.py

special instruction:

copyright 2022, MIT License, AditNW LLC

rev 1.0 initial creation
'''

import os

import config

# key objects filled by XXX_main.py
goop = None
machine = None
lcd_mgr = None

def save_life_cycles(cycles):
    _file_pathname = os.path.join(config.DATA_DIR, config.LIFE_CYCLES_FILENAME)
    with open(_file_pathname, "w") as file:
        file.write(str(cycles))

def get_life_cycles():
    _file_pathname = os.path.join(config.DATA_DIR, config.LIFE_CYCLES_FILENAME)
    with open(_file_pathname, "r") as file:
        return int(file.read())

def validate_data_dir():
    '''Create ./data if required
    Create life_cycle file
    '''
    # #### ./data
    if os.path.exists(config.DATA_DIR):
        pass
    else:
        os.makedirs(config.DATA_DIR)

    # #### life_cycles file
    _file_pathname = os.path.join(config.DATA_DIR, config.LIFE_CYCLES_FILENAME)
    with open(_file_pathname, "w") as file:
        file.write("0")