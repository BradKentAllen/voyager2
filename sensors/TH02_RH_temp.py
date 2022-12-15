#!/usr/bin/env python
'''
file name:  TH02_RH_temp.py
date created:  Dec 3, 2022
created by:  Brad Allen
project/support: voyager2               # root or script it supports
description:
    Support for TH02 temp and RH board from SEED studio
    Uses code found here:  https://github.com/ControlEverythingCommunity/TH02

special instruction:
    RH requires temp for calculation.  So only call get_temp_only if you only want the temp, otherwise,
    get the full meal deal with get_temp_RH


# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TH02
# This code is designed to work with the TH02_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'



import smbus
import time

class TH02:
    def __init__(self):
        # Get I2C bus
        self.bus = smbus.SMBus(1)
        self.I2C_address = 0x40

    def get_temp_only(self):
        '''use get_temp_RH if you want temp and RH
        '''
        # TH02 address, 0x40(64)
        # Select configuration register, 0x03(03)
        #       0x11(11)    Normal mode enabled, Temperature
        try:
            self.bus.write_byte_data(self.I2C_address, 0x03, 0x11)
        except OSError:
            return 'error', 'OSError'

        time.sleep(0.5)

        # TH02 address, 0x40(64)
        # Read data back from 0x00(00), 3 bytes
        # Status register, cTemp MSB, cTemp LSB
        data = self.bus.read_i2c_block_data(self.I2C_address, 0x00, 3)

        # Convert the data to 14-bits
        cTemp = ((data[1] * 256 + (data[2] & 0xFC))/ 4.0) / 32.0 - 50.0
        fTemp = cTemp * 1.8 + 32

        return cTemp, fTemp

    def get_temp_RH(self):
        '''temp is required in the RH calculations.
        This method returns both
        '''
        # #### get temp
        cTemp, fTemp = self.get_temp_only()
        if isinstance(cTemp, str):
            # sensor read error
            return 99, 99, 99

        # TH02 address, 0x40(64)
        # Select configuration register, 0x03(03)
        #       0x01(01)    Normal mode enabled, Relative humidity
        try:
            self.bus.write_byte_data(self.I2C_address, 0x03, 0x01)
        except OSError:
            return 99, 99, 99

        time.sleep(0.5)

        # TH02 address, 0x40(64)
        # Read data back from 0x00(00), 3 bytes
        # Status register, humidity MSB, humidity LSB
        data = self.bus.read_i2c_block_data(self.I2C_address, 0x00, 3)

        # Convert the data to 12-bits
        humidity = ((data[1] * 256 + (data[2] & 0xF0)) / 16.0) / 16.0 - 24.0
        humidity = humidity - (((humidity * humidity) * (-0.00393)) + (humidity * 0.4008) - 4.7844)
        humidity = humidity + (cTemp - 30) * (humidity * 0.00237 + 0.1973)

        return cTemp, fTemp, humidity


if __name__ == "__main__":
    app = TH02()

    while True:
        temp_C, temp_F, RH = app.get_temp_RH()
        # Output data to screen
        print(f"Relative Humidity : {RH:.2f}%")
        print(f"Temperature in Celsius : {temp_C:.2f} C")
        print(f"Temperature in Fahrenheit : {temp_F:.2f} F")
        print('\n')
        time.sleep(1)


