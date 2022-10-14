#!/usr/bin/env python
'''
file name:  LTA_goop.py
date created:  October 4, 2022
created by:  Brad Allen, AditNW LLC
project/support: Life Tester A      # root or script it supports
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
    ### Life Tester Parameters
    running = False
    mx = False
    fault = False
    run_direction = "stop" # 'stop', 'going up', 'going down'
    position = None  # 'None', 'passed_down', 'down', 'between', 'up', 'passed_up'
    life_cycles = 0
    session_cycles = 0




    #### general voyager2 parameters ####
    main_thread_inhibit: bool = False  # inhibits main thread, particular for button thread
    startup_seconds: int = 15 # must be greater than 10 seconds
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

    ''' init_UI flag
    if True, then will init UI.  Typically this includes new button functions
    '''
    init_UI: bool = False 


    