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

@dataclass
class Goop():
    ''' data
    '''
    ### Life Tester Parameters
    input_dict = {
        'input1': {'name': input1_name,
            'status': False,
            },
        'input2': {'name': input2_name,
            'status': False,
            },
        }

    output_dict = {
        'output1': {'name': output1_name,
            'status': False,
            },
        'output2': {'name': output2_name,
            'status': False,
            },
        }



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


    