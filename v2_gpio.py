#!/usr/bin/env python
'''
file name:  brain.py    #### Modem_Rider
date created:
created by:
project/support: voyager2 Modem_Rider   # root or script it supports
description:
    Brain contains all machine related objects such as gpio and sensor objects

special instruction:
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'

# load gpiozero functions, create list for later use
# https://gpiozero.readthedocs.io/en/stable/
from gpiozero import LED, Button, DigitalOutputDevice, DigitalInputDevice, Servo

#### Use pigpio pin factory
# pigpio is an alternative control for the RPi gpio
# pigpio provides more stable hardware pulse width modulations
# when using servos
# The pigpio daemon must be running for this to work
# To enable and will run on boot:
# sudo systemctl enable pigpiod

from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device
Device.pin_factory = PiGPIOFactory()


import config


class Machine:
    def __init__(self):
        # #### define gpio_zero objects
        # start with standard LED's
        self.gpio_objects = {
            'blue_LED_1': LED(config.RPi_PINOUT_BCM.get('blue_LED_1')),
            "blue_LED_2": LED(config.RPi_PINOUT_BCM.get('blue_LED_2')),
            "yellow_LED": LED(config.RPi_PINOUT_BCM.get('yellow_LED')),
            "red_LED": LED(config.RPi_PINOUT_BCM.get('red_LED')),
        }

        customizable_objects = {
            "i_o_4": None,
            "i_o_5": None,
            "i_o_8": None,
            "i_o_23": None,
            "i_o_24": None,

            "i_o_12": None,
            "i_o_16": None,
            "i_o_20": None,
        }

        # add custom pins
        for key, value in customizable_objects.items():
            if key in customizable_objects:
                if config.RPi_PINOUT_BCM[key].get('type') == "LED": 
                    self.gpio_objects[config.RPi_PINOUT_BCM[key].get('name')] = LED(config.RPi_PINOUT_BCM[key].get('pin'))
                elif config.RPi_PINOUT_BCM[key].get('type') == "Output":
                    self.gpio_objects[config.RPi_PINOUT_BCM[key].get('name')] = DigitalOutputDevice(config.RPi_PINOUT_BCM[key].get('pin'))
                elif config.RPi_PINOUT_BCM[key].get('type') == "Button":
                    self.gpio_objects[config.RPi_PINOUT_BCM[key].get('name')] = Button(config.RPi_PINOUT_BCM[key].get('pin'))
                else:
                    print('error v2_gpio: called output type that does not exist')
            else:
                print('error v2_gpio: called for key that is not in customizable objects')

        # #### define button actions
        #self.redefine_button_actions(self.button_1_default, self.button_2_default, self.button_3_default)

    def redefine_button_actions(self, button1_function, button2_function, button3_function):
        #print('### redefine_button_actions (in Machine/gpio')
        #print('looking at button1_function:')
        #print(button1_function.__name__)
        #print(type(button1_function))
        self.gpio_objects.get('button_1').when_pressed = button1_function
        self.gpio_objects.get('button_2').when_pressed = button2_function
        self.gpio_objects.get('button_3').when_pressed = button3_function

    def button_1_default(self):
        ''' runs all button functions by passing function into the method.
        '''
        print('>>> button 1 pressed <<<')

    def button_2_default(self):
        ''' runs all button functions by passing function into the method.
        '''
        print('>>> button 2 pressed <<<')

    def button_3_default(self):
        ''' runs all button functions by passing function into the method.
        '''
        print('>>> button 3 pressed <<<')

    def LED(self, name, state):
        ''' turn LED on or off using name and state
        name: name listed in config.RPI_PINOUT_BCM
        state:  ON or OFF
        '''
        state = state.upper()

        try:
            if state == "ON":
                self.gpio_objects.get(name).on()
            else:
                self.gpio_objects.get(name).off()
        except AttributeError:
            print('bad LED object passed in v2_gpio.py/LED')

    def output(self, name, state):
        ''' turn digital output on or off using name and state
        name: name listed in config.RPI_PINOUT_BCM
        state:  ON or OFF
        '''
        state = state.upper()

        try:
            if state == "ON":
                self.gpio_objects.get(name).on()
            else:
                self.gpio_objects.get(name).off()
        except AttributeError:
            print('bad digital output object passed in v2_gpio.py/output')
