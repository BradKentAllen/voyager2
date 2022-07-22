#!/usr/bin/env python
'''
file name: Modem_Rider_functions.py
date created: July 10, 2022
created by: Brad Allen
project/support: Modem Rider (voyager2)	# root or script it supports
description:

special instruction:
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'


def send_weather_text():
	phone_Brad = '14259856203'
	phone_Ann = '14254171516'
	try:
		from WeatherText import weather_text
	except Exception as e:
		print(f'error importing custom method: {e}')

	try:
		weather_text(phone_Brad, phone_Ann)
	except Exception as e:
		print(f'error running custom method: {e}')