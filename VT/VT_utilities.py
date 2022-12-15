#!/usr/bin/env python
'''
file name:  VTutilities.py
date created:  Dec 14, 2022
created by:  Brad Allen, AditNW LLC
project/support: Voyager2      # root or script it supports
description:  utitilities for import into DD_main.py

special instruction:

copyright 2022, MIT License, AditNW LLC

rev 1.0 initial creation
'''

import os
import datetime
import pickle

import config

# key objects filled by XXX_main.py
goop = None



# #########################
# #### Input Utilities ####
# #########################

def return_TMP36_temp(signal_mv, f_degrees=False):
    temp_C = ((signal_mv - 500) / 1000) * 100
    if f_degrees is False:
        return temp_C
    else:
        return (temp_C * 1.8) + 32




# #########################
# #### File Management ####
# #########################

def return_datetime_stamp():
    '''returns string of datetime in format for log
    '''
    return datetime.datetime.strftime(datetime.datetime.now(), '%m/%d %H:%M')


def validate_data_dir(file_path='data'):
    '''Create ./data if required
    Create life_cycle file
    '''
    # #### ./data
    if os.path.exists(file_path):
        pass
    else:
        os.makedirs(file_path)


def pickle_cache(data, file_name, file_path='data'):
    '''general method for caching a file
    '''
    # ### check file_name
    if '.pkl' in file_name:
        pass
    elif '.' in file_name:
        file_name = os.path.splitext(file_name)[0] + '.pkl'
    else:
        file_name = file_name + '.pkl'

    # ### save file
    file_pathname = os.path.join(file_path, file_name)

    with open(file_pathname, 'wb') as file:
        pickle.dump(data, file)

    return file_name


def get_pickled_cache(file_name, file_path='data'):
    '''general utility for loading pickled files from cache
    '''
    # ### check file_name
    if '.pkl' in file_name:
        pass
    elif '.' in file_name:
        file_name = os.path.splitext(file_name)[0] + '.pkl'
    else:
        file_name = file_name + '.pkl'

    file_pathname = os.path.join(file_path, file_name)

    try:
        with open(file_pathname, 'rb') as file:
            data_from_pickle = pickle.load(file)
    except pickle.UnpicklingError:
        return f'cache input file was not pickle: {file_name}'
    except FileNotFoundError:
        return f'no file at: {file_pathname} named {file_name}'

    return data_from_pickle














