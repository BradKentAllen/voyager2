#!/usr/bin/env python
'''
file name:  text_update.py
date created: Nov 2022
created by: Brad Allen
project/support:                # root or script it supports
description:

special instruction:
    Must have to support:
    Twilio_SMS.py
    giblets.py  # contains API info for Twilio
    weather_text.py
    tide_text.py
'''
__revision__ = 'vA.1'
__status__ = 'production' # 'DEV', 'alpha', 'beta', 'production'

from API.Twilio_SMS import send_SMS_message
from API.tide_text import Tide_Text
from API.weather_text import Weather_Text

from API.recipients import recipients_dict
from API.locations import locations_dict


class Text_Update:
    def __init__(self):
        self.DEBUG = False

        self.tide_app = Tide_Text()
        self.weather_app = Weather_Text()

        self.tide_text_list = []
        self.tide_text_dict = {}
        self.weather_text_list = []
        self.weather_text_dict = {}

    def collect_texts(self):
        '''to reduce API calls, this organizes the various texts into single
        calls.
        '''
        # #### Create list of locations for tides and weather
        for recipient, data in recipients_dict.items():
            if data.get('weather') is not None:
                self.weather_text_list.append(data.get('weather'))
            if data.get('tide') is not None:
                self.tide_text_list.append(data.get('tide'))

        # #### Get tide text data
        for location in self.tide_text_list:
            location_data = locations_dict.get(location)
            if location_data is not None:
                station_ID = location_data.get('tide_station')
                if station_ID is not None:
                    self.tide_text_dict[location] = self.tide_app.get_tide(
                        station=station_ID,
                        station_name=location.split(',')[0],
                        )

        # #### Get weather text data
        for location in self.weather_text_list:
            location_data = locations_dict.get(location)
            if location_data is not None:
                city_ID = location_data.get('openweathermap')
                if city_ID is not None:
                    self.weather_text_dict[location] = self.weather_app.get_weather(
                        city_ID=city_ID,
                        city_name=location.split(',')[0],
                        )

    def send_tide_texts(self):
        '''send collected texts to recipients
        '''
        for recipient, data in recipients_dict.items():
            if data.get("tide") is not None:
                if self.DEBUG is False:
                    send_SMS_message(
                        message=self.tide_text_dict.get(data.get("tide")),
                        phone_number=data.get("phone"),
                        )
                else:
                    print(f'send to {data.get("phone")}')
                    print(f'sent this: \n{self.tide_text_dict.get(data.get("tide"))}\n')

    def send_weather_texts(self):
        for recipient, data in recipients_dict.items():
            if data.get("weather") is not None:
                if self.DEBUG is False:
                    send_SMS_message(
                        message=self.weather_text_dict.get(data.get("weather")),
                        phone_number=data.get("phone"),
                        )
                else:
                    print(f'send to {data.get("phone")}')
                    print(f'sent this: \n{self.weather_text_dict.get(data.get("weather"))}\n')


if __name__=='__main__':
    app = Text_Update()

    app.DEBUG = True

    app.collect_texts()
    app.send_tide_texts()
    app.send_weather_texts()







