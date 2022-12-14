#!/usr/bin/env python
'''
file name:  weather_text.py
date created: Nov 2022 based on WeatherText.py
created by: Brad Allen
project/support:                # root or script it supports
description:

special instruction:
    Uses Open Weather API to get forecast
    Formats forecast for nice looking text


    Returns the weather text ready to run in Twilio
    Does not send text

    gets weather data from openweathermap.org
    download city list here:  http://bulk.openweathermap.org/sample/

    Fort Wayne:  4920423
    Columbia City:  4919203
    Tacoma:  5812944
    Gig Harbor:  5795440




'''
__revision__ = 'vA.1'
__status__ = 'production' # 'DEV', 'alpha', 'beta', 'production'

from datetime import datetime
import requests
import json
import signal

import giblets



class Weather_Text():
    def __init__(self):  # default is for Tacoma
        pass
        
    
    def get_weather_JSON(self, city_ID, city_name):
        '''
        
        '''
        # cityID = 5789198 # Carnation
        API = giblets.open_weather_API

        # this line will not work below python 3.6
        URL = f'https://api.openweathermap.org/data/2.5/forecast?id={city_ID}&APPID={API}'
        response = requests.get(URL)

        # use requests built in error handling
        response.raise_for_status()

        # load json into data object
        weather_data = json.loads(response.text)

        return weather_data

    def get_weather(self, city_ID, city_name=None):
        '''
        create day's weather overview
        return as weatherString
        '''
        weather_data = self.get_weather_JSON(city_ID, city_name)

        weatherString = ''
        for count, item in enumerate(weather_data['list']):
            tempF = (((float(item['main']['temp'])) - 273) * 1.8) + 32

            if count == 0:
                thisTime = datetime.strptime(item['dt_txt'],'%Y-%m-%d %H:%M:%S')
                weatherString = weatherString + thisTime.strftime('%a, %b %d') + '\n'
            hour = int(item['dt_txt'][11:-6])

            # convert time of day in forecast to string time frames
            # adjusted for time being in UTC
            timeOfDay = {9: 'midnight', 12: 'early', 15: 'early', 18: 'morng', 21: 'noon ', 0: 'aftrn', 3:'eveng', 6: 'night'}
            #timeOfDay = {0: 'midnight', 3: 'early', 6: 'early', 9: 'morng', 12: 'noon ', 15: 'aftrn', 18:'eveng', 21: 'night'}

            # shorten descriptions for text format:
            modDescription = {
                'overcast clouds': 'overcast',
                'scattered clouds': 'sctrd clouds',
                'broken clouds': 'brkn clouds',
                'light rain': 'lt rain',
                'moderate rain': 'med rain',
                'heavy intensity rain': 'hvy rain',
                'very heavy rain': 'hvy rain',
                'extreme rain': 'ext rain',
                'freezing rain': 'frzng rain',
                'light intensity shower rain': 'lt showers',
                'shower rain': 'showers',
                'heavy intensity shower rain': 'hvy showers',
                'ragged shower rain': 'showers',
                }
            condition = ''
            if item['weather'][0]['description'] in modDescription:
                condition = modDescription[item['weather'][0]['description']]
            else:
                condition = item['weather'][0]['description']

            if hour in [0, 3, 6, 15, 18, 21]:
                try:
                    weatherString = weatherString + timeOfDay[hour]
                    weatherString = weatherString + ' ' + '{:.0f}'.format(tempF)
                    weatherString = weatherString + ' ' + condition + '\n'
                except KeyError:
                    weatherString = weatherString + ' error' + '\n'
            # count = 6 gives one days results
            if count > 6:
                break

        return weatherString


def keyboardInterruptHandler(signal, frame):
    '''safe handle ctl-c stop'''
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)


if __name__ == '__main__':
        print('starting')
        # react to keyboard interrupt
        signal.signal(signal.SIGINT, keyboardInterruptHandler)
        app = Weather_Text()

        print(app.get_weather(city_ID=4164138))

        #print(app.get_weather())
        '''
        for item in app.get_weather_JSON().get('list'):
            print(item)
            if item.get('rain') is not None:
                print(f"\n>>> {item.get('dt_txt')}: ", end='')
                print(f"rain: {item.get('rain')}")
        '''

        print('end script')

