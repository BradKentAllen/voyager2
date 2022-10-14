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

timers_dict = {
    "up stop timer": {
        "status": "wait",  # "wait", "run", "stop"
        "time count": 0,
        "trigger count": 10,
        "trigger action": ("run_direction", "going_down")
        }
    }

def reset_timer(_timer):
    _timer["status"] = "wait"
    _timer["count"] = 0
    return _timer

# ###################
# #### Run Logic ####
# ###################

def new_actions_dict():
    return {
        "fault": None,
        "run direction": None,
        }

def run_logic(up_limit_switch, down_limit_switch):
    '''Main logic for running life test.
    Turns flags on and off but does not drive gpio
    Drive gpio separately.
    '''
    print(f'\nrun logic:')
    print(f'{up_limit_switch}, {down_limit_switch}')
    print(f'{goop.running}, {goop.run_direction}, {goop.position}')

    # #### Faults ####
    if up_limit_switch is True and down_limit_switch is True:
        actions_dict["fault"] = 'Both limit switches are engaged'
        return actions_dict

    # set up clean actions_dict
    actions_dict = new_actions_dict()

    # ### position based actions
    if up_limit_switch is True:
        if goop.run_direction == "going up":
            print('>> start up stop timer')
            # arrived at top, trigger timer to go down
            goop.run_direction = "stop"
            goop.position = "up"
            timers_dict['up stop timer']['status'] = "run"
    elif down_limit_switch is True:
        pass
    else:
        pass


     # ### timer based actions
    for _timer, attr_dict in timers_dict.items():
        print(f'\n{attr_dict}')
        if attr_dict['status'] == "run":
            print(f'increment: {_timer}')
            attr_dict['time count'] +=1
            if attr_dict['time count'] >= attr_dict['trigger count']:
                print(f'!!! trigger {_timer}')
                actions_dict[attr['trigger action'][0]] = attr['trigger action'][0]

    return actions_dict



    

def find_initial_position(up_limit_switch, down_limit_switch):
    '''logic to fill goop.position
    Returns "up", "down", or "between"
    ''' 
    # #### Faults ####
    if up_limit_switch is True and down_limit_switch is True:
        return 'Fault: Both limit switches are engaged'

    if up_limit_switch is True:
        goop.position = 'up'
        goop.run_direction = 'stop'
    elif down_limit_switch is True:
        goop.position = 'down'
        goop.run_direction = 'stop'

    else:
        goop.position = 'between'
        # XXXX change to 'going_down'
        goop.run_direction = 'going_up'

    return "good"




# #########################
# #### File Management ####
# #########################

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