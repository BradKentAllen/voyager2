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
    # settings
    running = False
    mx = False
    fault = False
    count_cycle = False  # cycles are counted at bottom, must run down first
    position = None  # 'None', 'passed_down', 'down', 'between', 'up', 'passed_up'


    # dynamic test parameters (set within the code)
    current_timer = 0  # current stage timer value

    test_stage = None
    test_process = {}

    # logged data parameters (LTA_util write_one_log_line and write_column_names must 
    # be set up consistently)
    life_cycles = 0
    session_cycles = 0
    up_time = 0
    motor_temp = 0
    ambient_temp = 0

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


    