#!/usr/bin/env python
'''
file name:  multimeter_utility.py
date created:  August 25, 2022
created by: Brad Allen
project/support: voyager2      # root or script it supports
description:  Full package for ina219 multimeter breakout

https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/python-circuitpython

this is an alternative library
https://pypi.org/project/pi-ina219/

Runs as an indendent self-test as well

rev 0.0.1 initial DEV
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'

import board
import busio
import adafruit_ina219
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ina219.INA219(i2c)

print("Bus Voltage:   {} V".format(ina219.bus_voltage))
print("Shunt Voltage: {} mV".format(ina219.shunt_voltage / 1000))
print("Current:       {} mA".format(ina219.current))

