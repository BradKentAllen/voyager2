#!/usr/bin/env python
'''
file name:  tide_text.py
date created: Nov 2022
created by: Brad Allen
project/support:                # root or script it supports
description:

special instruction:
    Uses NOAA tide API, free no key required

rev:  (11/25/22) - error response if URL does not work


'''
__revision__ = 'vA.1'
__status__ = 'production' # 'DEV', 'alpha', 'beta', 'production'

import datetime
import requests
import json
import signal
import math



class Tide_Text():
    def __init__(self):  # default is for Tacoma
        self.begin_date = datetime.datetime.now().strftime("%Y%m%d") # (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
        self.time_range = 36
        self.product = 'predictions'
        self.interval = 'hilo'  # some stations can only provide hilo
        self.units = 'english'  # metric

    def get_tide_JSON(self, station, station_name):
        '''returns json from API for use in other methods
        '''
        self.station_name = station_name

        url = f'https://tidesandcurrents.noaa.gov/api/datagetter?begin_date={self.begin_date}&range={self.time_range}&product={self.product}\
        &datum=mllw&interval={self.interval}&format=json&units={self.units}&time_zone=lst_ldt&station={station}'

        #url = 'dogs'
        try:
            response = requests.get(url)
        except Exception as e:
            return "no url response"

        # use requests built in error handling
        response.raise_for_status()

        # load json into data object
        tide_data = json.loads(response.text)

        return tide_data

    def get_tide(self, station=9446491, station_name='Arletta'):
        '''
        create day's tide prediction
        return as tide_string formatted for SMS text
        '''
        tide_data = self.get_tide_JSON(station, station_name)

        # this will be an error
        if isinstance(tide_data, str):
            return tide_data

        tide_list = tide_data.get('predictions')

        tide_string = f"tides for {self.station_name}\n{datetime.datetime.now().strftime('%a %b %d')}\n" 

        for item in tide_list:
            time = item.get('t')
            time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
            height = float(item.get('v'))
            tide_string = tide_string + f"{time.strftime('%l:%M %p')}: {item.get('type')}, {height:.1f}\n"

        return tide_string

    def get_tide_dict(self, station=9446491, station_name='Arletta'):
        ''' returns a dictionary of information for predicting tide height

        Checks values and returns None for invalid data
        '''
        tide_data = self.get_tide_JSON(station, station_name)

        # this will be an error
        if isinstance(tide_data, str):
            return tide_data

        tide_list = tide_data.get('predictions')

        tide_dict = {}

        for count, item in enumerate(tide_list):
            tide_dict[count + 1] = {}

            # time
            _time = item.get('t')
            if _time is None:
                return None
            try:
                tide_dict[count + 1]['time'] = datetime.datetime.strptime(_time, '%Y-%m-%d %H:%M')
            except ValueError:
                return None

            # height
            _height = item.get('v')

            if _height is None:
                return None

            try:
                tide_dict[count + 1]['height'] = float(_height)
            except ValueError:
                return None

            # tide type ('H' or 'L')
            _tide_type = item.get('type')

            if _tide_type is None:
                return None

            if _tide_type in ('H', 'L'):
                tide_dict[count + 1]['tide_type'] = _tide_type
            else:
                return None

        return tide_dict


def tide_LCD(tide_dict, previous_tide_data=None, tide_max=15.7, tide_min=-4, display_range=16, debug=False):
    '''returns character string for use in LCD

    previous_tide data is the previous_key data from the last time through

    debug allows testing with print instead of LCD
    '''
    # tide_dict will be None if there is any bad data in the tide json
    if tide_dict is None:
        return 'no tide data'

    '''
    print('\n\n>>>>>>>>>>')
    print(datetime.datetime.strftime(datetime.datetime.now(), '%H:%M'))
    '''

    # #### Find which two tides you are between
    previous_key = 0
    for key, value in tide_dict.items():
        #print(f'{key}: {value}')
        if datetime.datetime.now() <= value.get('time'):
            break

        previous_key = key

    #print(f'\ntide is betwen {previous_key} and {key}')

    # #### Deal with first tide period after midnight
    if previous_key == 0:
        tide_dict[0] = previous_tide_data


    # use keys to get tides at start and finish of 
    start_tide_dict = tide_dict[previous_key]
    end_tide_dict = tide_dict[key]

    '''
    print('\n start_tide_dict:')
    print(start_tide_dict)
    print('\n end_tide_dict:')
    print(end_tide_dict)
    '''
    

    minutes_span = int(((end_tide_dict.get('time') - start_tide_dict.get('time')).total_seconds()/60))

    tide_minutes = int(((datetime.datetime.now() - start_tide_dict.get('time')).total_seconds()/60))

    tide_span = (end_tide_dict.get('height')) - (start_tide_dict.get('height'))

    # determine which portion of sine wave to use
    sine_offset = 1.5

    # position on sine wave
    try:
        i = math.pi * (sine_offset + (tide_minutes / minutes_span))
    except ZeroDivisionError:
        i = 0

    # get actual value
    # offset the sine wave up (0 to 2) then divide to get (0 to 1)
    sine_x = (math.sin(i) + 1.0) / 2

    # use the sine and the full tide span to get the current height
    tide_height = (sine_x * tide_span) + start_tide_dict.get('height')

    #print(f'tide_minutes: {(tide_minutes):.0f}: {sine_x:.2f}')
    #print(f'{tide_span=}, tide height: {tide_height:.1f}')

    display_list = ['-', '-', '-', '0', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+']
    
    display_range_increment = (tide_max - tide_min) / display_range

    display_index = int((tide_height - tide_min) / display_range_increment)
    #print(f'{display_index=}')

    next_tide_index = int((end_tide_dict.get('height') - tide_min) / display_range_increment)
    #print(f'{next_tide_index=}')

    #print('^^^^^^^^^^^^^^^^^^')

    # place current tide mark
    if start_tide_dict.get('tide_type').lower() == 'h':
        mark = '<'
    else:
        mark = '>'

    display_list[display_index] = mark

    # place makr and erase characters above current
    final_display_list = []
    for count, char in enumerate(display_list):
        if count < display_index:
            final_display_list.append(char)
        elif count == display_index:
            final_display_list.append(mark)
        else:
            final_display_list.append('_')

    # place next tide
    if start_tide_dict.get('tide_type').lower() == 'h':
        next_tide_mark = 'L'
    else:
        next_tide_mark = 'H'

    final_display_list[next_tide_index] = next_tide_mark

    display = ''.join(final_display_list)



    return {
        'display string': display,
        'char list': final_display_list,
        'tide height': tide_height,
        'next tide': next_tide_mark,
        'next tide height': end_tide_dict.get('height'),
        'next tide time': end_tide_dict.get('time'),
        'previous tide data': start_tide_dict,
        }


def keyboardInterruptHandler(signal, frame):
    '''safe handle ctl-c stop'''
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)


if __name__ == '__main__':
        print('starting')
        # react to keyboard interrupt
        signal.signal(signal.SIGINT, keyboardInterruptHandler)
        app = Tide_Text()

        #print(app.get_tide_dict())

        app.time_range = 36
        for key, value in app.get_tide_dict().items():
            print(f'\n{key}:')
            for key2, value2 in value.items():
                print(f'{key2}: {value2}')

        print('end script')

