#!/usr/bin/env python
'''
file name:  heel_utility.py
date created:  August 24, 2022
created by: Brad Allen
project/support: voyager2 / NomiNomi      # root or script it supports
description:  Full package to heel from ADXL345

Heel to Port is Negative
Heel to Starboard is Positive

Runs as an indendent self-test as well

rev 0.0.1 initial DEV
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'

import time
import math

import board
import busio

import adafruit_adxl34x


def calc_roll_angle(accel_X):
    accel_X = float(accel_X)
    gravity = 9.8
    if (-1 * gravity) <= accel_X <= gravity:
        roll_angle_rad = math.asin(accel_X / gravity)
        roll_angle = 180 * roll_angle_rad / math.pi
    else:
        roll_angle = 90

    return int(roll_angle)


def get_radians(degrees):
    return (degrees * math.pi/180)

class ADXL345:
    def __init__(self):
        '''ADXL345 is fixed I2C address of 0x53 in Adafruit library
        '''
        # instantiate sensor object
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_adxl34x.ADXL345(i2c)
        
        self.acc_X = 0.0
        self.acc_Y = 0.0
        self.acc_Z = 0.0  

    def update_data(self):
        '''Read sensor using sensor driver
        DeviceRangeError returns ???
        '''
        try:
            acceleration_XYZ = self.sensor.acceleration
        except OSError:
            self.err_log.log_error(f'ADXL345 acclerometer did not read correctly')

        self.acc_X = acceleration_XYZ[0]
        self.acc_Y = acceleration_XYZ[1]
        self.acc_Z = acceleration_XYZ[2]



    def get_acc_X(self, update=True, format=True):
        '''Primary method for getting X acceleartion
        update=False saves processing if other data was collected first
        '''
        if update == True:
            self.update_data()

        if format == True:
            return f'{self.acc_X:.1f}'
        else:
            return self.acc_X

    def get_acc_Y(self, update=True, format=True):
        '''Primary method for getting X acceleartion
        update=False saves processing if other data was collected first
        '''
        if update == True:
            self.update_data()

        if format == True:
            return f'{self.acc_Y:.1f}'
        else:
            return self.acc_Y

    def get_acc_Z(self, update=True, format=True):
        '''Primary method for getting X acceleartion
        update=False saves processing if other data was collected first
        '''
        if update == True:
            self.update_data()

        if format == True:
            return f'{self.acc_Z:.1f}'
        else:
            return self.acc_Z


if __name__ == "__main__":
    print('\nTest heel_utlity.py and ADXL345')
    heel_sensor = ADXL345()
    while True:
        X_accel = heel_sensor.get_acc_X(True, True)
        print(f'acc x: {X_accel}')
        print(f'angle: {calc_roll_angle(X_accel)}')
        time.sleep(1)





