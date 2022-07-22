#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LCD_I2C.py

'''
Based on I2C_LCD_driver5.py
which was originally heavily modified code found at:
https://gist.github.com/DenisFromHR/cc863375a6e19dce359d


"""
Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic
Made available under GNU GENERAL PUBLIC LICENSE

CUSTOM CHARACTERS:

# CUSTOM CHARACTERS
customCharacters = [
    # Char 0 - GPS
    [0x11, 0x0a, 0x4, 0x1f, 0x11, 0x11, 0x1f, 0x0e],
    # Char 1 - water drop 
    [0x0, 0x4, 0x4, 0xa, 0x11, 0x11, 0x11, 0xe],
    # Char 2 - up arrow
    [0x0, 0x4, 0xe, 0x1f, 0x0, 0x1f, 0x0, 0x0],
    # Char 3 - down arrow
    [0x0, 0x0, 0x1f, 0x0, 0x1f, 0xe, 0x4,  0x0]
    ]

self.custom = {
    'GPS': 0,
    'water drop': 1,
    'up arrow': 2,
    'down arrow': 3
    }

# load custom characters
self.mylcd.lcd_load_custom_chars(customCharacters)
'''

# rev 0.1 - DEV from I2C_LCD_driver5.py

#### SETUP INFO ####


# LCD Address
# given in function call
#ADDRESS = 0x27
#ADDRESS = 0x23
#ADDRESS = config.LCDaddress

import smbus
from time import sleep

# customized config
import my_RPi_config as config

#### this is a hardware utility, not the function call
class i2c_device:
    '''utility function for I2C hardware
    '''
    def __init__(self, addr):
        I2CBUS = 1  # This only varied with RPi version 1
        self.addr = addr
        self.bus = smbus.SMBus(I2CBUS)

    # Write a single command
    def write_cmd(self, cmd):
        self.bus.write_byte(self.addr, cmd)
        sleep(0.0001)

    # Write a command and argument
    def write_cmd_arg(self, cmd, data):
        self.bus.write_byte_data(self.addr, cmd, data)
        sleep(0.0001)

    # Write a block of data
    def write_block_data(self, cmd, data):
        self.bus.write_block_data(self.addr, cmd, data)
        sleep(0.0001)

    # Read a single byte
    def read(self):
        return self.bus.read_byte(self.addr)

    # Read
    def read_data(self, cmd):
        return self.bus.read_byte_data(self.addr, cmd)

    # Read a block of data
    def read_block_data(self, cmd):
        return self.bus.read_block_data(self.addr, cmd)


# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit


#### This is the actual function call
class LCD:
    #### Stock LCD functions ####
    #initializes objects and lcd
    def __init__(self, LCDaddress=0):
        '''LCD class for 2 or 4 line lcd display
        '''
        # this allows assigning a second LCD
        if LCDaddress == 0:
            LCDaddress = config.I2C_LCD_ADDRESS
        self.lcd_device = i2c_device(LCDaddress)

        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)

        self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        sleep(0.2)


    # clocks EN to latch command
    def lcd_strobe(self, data):
        self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
        sleep(.0005)
        self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
        sleep(.0001)

    def lcd_write_four_bits(self, data):
        self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
        self.lcd_strobe(data)

    ################################
    ### Methods Required for API ###
    ################################

    # write a command to lcd
    def lcd_write(self, cmd, mode=0):
        '''lcd_write is referenced as a lower level function
        at several points.
        '''
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))


    # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
    def write_char(self, charvalue, mode=1):
        '''write_char is referenced by several lower level functions and 
        is referenced by the API
        '''
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

    
    def write_string(self, string, line=1, pos=0):
        '''Main String Write Function
        Lines numbered 1-4
        Positions start at 0
        '''
        if line == 1:
            pos_new = pos
        elif line == 2:
            pos_new = 0x40 + pos
        elif line == 3:
            pos_new = 0x14 + pos
        elif line == 4:
            pos_new = 0x54 + pos

        self.lcd_write(0x80 + pos_new)

        for char in string:
            self.lcd_write(ord(char), Rs)
    

    # clear lcd and set to home
    def clear(self):
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_RETURNHOME)

    # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
    def backlight(self, state): # for state, 1 = on, 0 = off
        if state == 1:
           self.lcd_device.write_cmd(LCD_BACKLIGHT)
        elif state == 0:
           self.lcd_device.write_cmd(LCD_NOBACKLIGHT)

