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
    print(f'up switch: {up_limit_switch}, down switch: {down_limit_switch}')
    print(f'stage: {goop.test_stage}')

    _stage_data = goop.test_process.get(goop.test_stage)
    _action = None
    _update_UI = False
    _status = "good"

    # #### Faults ####
    if up_limit_switch is True and down_limit_switch is True:
        actions_dict["fault"] = 'Both limit switches are engaged'
        return actions_dict

    # #### react to triggers
    if _stage_data.get("trigger time") == "up limit switch" and up_limit_switch is True:
        _status = next_test_stage()
        _stage_data = goop.test_process.get(goop.test_stage)
        _update_UI = True


    elif _stage_data.get("trigger time") == "down limit switch" and down_limit_switch is True:
        _status = next_test_stage()
        _stage_data = goop.test_process.get(goop.test_stage)
        _update_UI = True

    elif isinstance(_stage_data.get("trigger time"), int) and _stage_data.get("trigger time") <= _stage_data.get("timer"):
        _status = next_test_stage()
        _stage_data = goop.test_process.get(goop.test_stage)
        _update_UI = True

    else:
        # #### perform current stage action
        _action = _stage_data.get("action")
        _stage_data = goop.test_process.get(goop.test_stage)

        if goop.screen_message != _stage_data.get("message"):
            goop.screen_message = _stage_data.get("message")
            _update_UI = True
            


    goop.test_process[goop.test_stage]["timer"] +=1

    if _status == "fault":
        return "fault", _stage_data.get("log name")

    return _update_UI, _action


def next_test_stage():
    '''process finish actions from stage and start next stage
    '''
    # execute trigger actions from current stage
    _stage_data = goop.test_process.get(goop.test_stage)
    if _stage_data.get("trigger action") == "fault":
        return "fault"

    _this_stage = False
    _found = False
    for _stage_name, _stage_data in goop.test_process.items():
        if _this_stage is True:
            goop.test_stage = _stage_name
            _found = True
            break
        if _stage_name == goop.test_stage:
            _this_stage = True

    if _found is False:
        # roll to top of dict
        goop.test_stage = next(iter(goop.test_process))

    # initialize key parameters in new stage
    _stage_data = goop.test_process.get(goop.test_stage)

    goop.screen_message = _stage_data.get("message")

    return "good"


def determine_initial_stage():
    '''uses initial position to determine which stage in test_process to
    start with
    '''
    for _stage, _data in goop.test_process.items():
        # XXXX create logic
        pass

    return "1 up cycle"

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