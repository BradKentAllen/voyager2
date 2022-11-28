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
import datetime

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

def reset_timer():
    '''reset timer in current stage
    '''
    goop.test_process[goop.test_stage]["timer"] = 0
    

def run_logic(up_limit_switch, down_limit_switch):
    '''Main logic for running life test.
    Turns flags on and off but does not drive gpio
    Drive gpio separately.
    '''
    if config.DEBUG is True:
        print(f'\nrun logic:')
        print(f'up switch: {up_limit_switch}, down switch: {down_limit_switch}')
        print(f'stage: {goop.test_stage}')

    _stage_data = goop.test_process.get(goop.test_stage)
    _action = None
    _update_UI = False
    _status = "good"

    # #### Faults ####
    if up_limit_switch is True and down_limit_switch is True:
        fault_msg = '2x switches engaged'
        return "fault", fault_msg
    elif goop.test_process[goop.test_stage]["fault time"] is not None:
        if goop.test_process[goop.test_stage]["timer"] >= goop.test_process[goop.test_stage]["fault time"]:
            fault_msg = goop.test_process[goop.test_stage]["fault message"]
            return "fault", fault_msg

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
        # #### Timer Execution and Reset
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
            

    # increment the main stage time
    goop.test_process[goop.test_stage]["timer"] +=1

    # set current_timer for display
    goop.current_timer = goop.test_process[goop.test_stage]["timer"]

    if _status == "fault":
        return "fault", _stage_data.get("log name")

    return _update_UI, _action

def log_cycles():
    # count cycles only after a full cycle
    if goop.count_cycle is False:
        goop.count_cycle = True
    else:
        goop.life_cycles +=1
        goop.session_cycles +=1

def next_test_stage():
    '''process finish actions from stage and start next stage
    '''
    # execute trigger actions from current stage
    _stage_data = goop.test_process.get(goop.test_stage)
    if _stage_data.get("trigger action") == "fault":
        return "fault"
    elif _stage_data.get("trigger action") == "log cycles":
        log_cycles()
    elif _stage_data.get("trigger action") == "log timer":
        goop.up_time = _stage_data.get("timer")
    elif _stage_data.get("trigger action") == "log timer and cycles":
        goop.up_time = _stage_data.get("timer")
        log_cycles()



    reset_timer()

    # #### convert to next stage
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

    XXXX - problems here including logic and use of actual cycle name
    '''
    for _stage, _data in goop.test_process.items():
        if "down cycle" in _stage:
            return _stage

    return _stage

def find_initial_position(up_limit_switch, down_limit_switch):
    '''logic to fill goop.position
    Returns "up", "down", or "between"
    ''' 
    # #### Faults ####
    if up_limit_switch is True and down_limit_switch is True:
        return 'Fault: Both limit switches are engaged'

    if up_limit_switch is True:
        goop.position = 'up'
    elif down_limit_switch is True:
        goop.position = 'down'
    else:
        goop.position = 'between'

    return "good"




# #########################
# #### File Management ####
# #########################

def return_datetime_stamp():
    '''returns string of datetime in format for log
    '''
    return datetime.datetime.strftime(datetime.datetime.now(), '%m/%d %H:%M')

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

def write_column_names(file):
    for _column in config.LOG_COLUMNS:
        file.write(f'{_column}, ')
    file.write('\n')

def log_new_session():
    _file_pathname = os.path.join(config.DATA_DIR, config.LOG_FILENAME)
    with open(_file_pathname, "a") as file:
        file.write('\n')
        file.write(f'New Session: {return_datetime_stamp()}\n')
        write_column_names(file)

def validate_log_file():
    '''makes sure log file is present, creates if not
    Should be preceded by validate_data_dir
    '''
    _file_pathname = os.path.join(config.DATA_DIR, config.LOG_FILENAME)
    try:
        with open(_file_pathname, "r") as file:
            pass
    except FileNotFoundError:
        with open(_file_pathname, "w") as file:
            write_column_names(file)

    else:
        log_new_session()
            

def write_one_log_line():
    _file_pathname = os.path.join(config.DATA_DIR, config.LOG_FILENAME)
    with open(_file_pathname, "a") as file:
        file.write(f'{return_datetime_stamp()}, ')
        file.write(f'{goop.life_cycles}, ')
        file.write(f'{goop.session_cycles}, ')
        file.write(f'{goop.up_time}, ')
        file.write(f'{goop.motor_temp:.0f}, ')
        file.write(f'{goop.ambient_temp:.0f}, ')
        file.write('\n')


def write_fault_log_line(fault_msg):
    _file_pathname = os.path.join(config.DATA_DIR, config.LOG_FILENAME)
    with open(_file_pathname, "a") as file:
        file.write(f'{return_datetime_stamp()}, ')
        file.write(f'{fault_msg}, ')
        file.write('\n')

def return_TMP36_temp(signal_mv, f_degrees=False):
    temp_C = ((signal_mv - 500) / 1000) * 100
    if f_degrees is False:
        return temp_C
    else:
        return (temp_C * 1.8) + 32

















