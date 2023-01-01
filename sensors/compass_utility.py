#!/usr/bin/env python
'''
file name:  compass_utility.py
date created:  August 22, 2022
created by: Brad Allen
project/support: voyager2 / NomiNomi      # root or script it supports
description:  Full package to read BNo055

Runs as an indendent self-test as well

rev 0.0.1 initial DEV
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'

import time
import board
import busio
import adafruit_bno055


class BNo055:
    def __init__(self, sensor_mgr):
        self.mgr = sensor_mgr
        '''BNo055 is fixed I2C address of 0x28 in Adafruit library
        '''
        # instantiate sensor object
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        
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

        #print("Accelerometer (m/s^2): {}".format(self.sensor.acceleration))
        #print("Magnetometer (microteslas): {}".format(self.sensor.magnetic))
        #print("Gyroscope (rad/sec): {}".format(self.sensor.gyro))
        #print("Euler angle: {}".format(self.sensor.euler))
        #print("Quaternion: {}".format(self.sensor.quaternion))
        #print("Linear acceleration (m/s^2): {}".format(self.sensor.linear_acceleration))
        #print("Gravity (m/s^2): {}".format(self.sensor.gravity))
        #print()

        # sensor.acceleration returns: (x, y, z)
        # sensor.euler returns: (bearing, ?, ?)

    def get_acceleration(self):
        return self.sensor.acceleration

    def get_euler(self):
        return self.sensor.euler

class Compass:
    def __init__(self):
        self.sense_BNo055 = BNo055(self)

    def read_compass_bearing(self):
        euler = self.sense_BNo055.get_euler()
        if euler[0] is not None:
            if 0 <= euler[0] <= 360:
                return int(euler[0])

        return 999

if __name__ == "__main__":
    print('\nRun compass test utility')
    compass = Compass()
    while True:
        print(f'heading: {compass.read_compass_bearing()}')
        time.sleep(4)





