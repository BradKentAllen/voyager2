#!/usr/bin/env python
'''
file name:  DD_goop.py
date created:  November 19, 2022
created by:  Brad Allen, AditNW LLC
project/support: DataDog      # root or script it supports
description:

special instruction:

copyright 2022, MIT License, AditNW LLC

rev 1.0 initial creation from MR_UI.py
'''


from dataclasses import dataclass

import config

@dataclass
class Goop():
    ''' data
    '''
    ### DataDog Parameters
    # settings
    running = False
    mx = False
    fault = False
    fault_msg = 'no fault'
    os_operation = None # None, 'reboot', 'shut down'

    tide_data_dict = None

    temp_in = 99
    temp_out = 99
    pressure = 99
    RH = 0
    dew_point = 0


    #### general voyager2 parameters ####
    main_thread_inhibit: bool = False  # inhibits main thread, particular for button thread
    startup_seconds: int = 10 # must be greater than 5 seconds
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
    current_screen_group: str = 'home'
    current_screen: str = 'main'

    screen_message: str = 'Loading'

    ''' init_UI flag
    if True, then will init UI.  Typically this includes new button functions
    '''
    init_UI: bool = False 


    