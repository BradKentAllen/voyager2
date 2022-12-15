#!/usr/bin/env python
'''
file name:  DHT22_RH.py
date created:  Dec 1, 2022
created by: Brad Allen
project/support: Voyager 2               # root or script it supports
description:
    Sensor file for running DHT22 temp and relative humidity sensor

special instruction:
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV'  # 'DEV', 'alpha', 'beta', 'production'

import time

import adafruit_dht
import board


dhtDevice = adafruit_dht.DHT22(board.D18)

while True:
    try:
        # Print the values to the serial port
        print(type(dhtDevice.temperature))
        print(f'{dhtDevice.temperature=}')
        temperature_c = dhtDevice.temperature
        if temperature_c is not None:
            temperature_f = temperature_c * (9 / 5) + 32
        else:
            temperature_f = 99
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except OverflowError as error:
        print(" DHT - " + str(error))
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

