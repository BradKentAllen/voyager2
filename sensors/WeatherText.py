# WeatherText.py
'''Uses Open Weather API to get forecast
Formats forecast for nice looking text
Sends using Nexmo
Requires config.py for Nexmo keys
'''

from datetime import datetime
import requests
import json
import signal

# must be in folder
import config
import NEXMOmessage as nexmo


class weather_text():
    def __init__(self):
        weatherData = self.getWeatherJSON()
        weatherString = self.getWeather(weatherData)
        nexmo.sendNexmoSMS(weatherString, config.phoneBrad, config.phoneAnn)
    
    def getWeatherJSON(self):
        '''
        gets weather data from openweathermap.org
        saves as LatestForecast.json
        '''
        cityID = 5789198
        API = '32c27777152e3fa00b10f320b4cf3a9d'

        # this line will not work below python 3.6
        URL = f'https://api.openweathermap.org/data/2.5/forecast?id={cityID}&APPID={API}'
        response = requests.get(URL)

        # use requests built in error handling
        response.raise_for_status()

        # load json into data object
        weather_data = json.loads(response.text)

        return weather_data

    def getWeather(self, weather_data):
        '''
        create day's weather overview
        return as weatherString
        '''
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
        weather_text()

        print('end script')

