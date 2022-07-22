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
'''
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device
Device.pin_factory = PiGPIOFactory()
'''

import config


class Machine:
    def __init__(self):
        # define gpio_zero objects
        self.gpio_objects = {
            'blue_LED_1': LED(config.RPi_PINOUT_BCM.get('blue_LED_1')),
            "blue_LED_2": LED(config.RPi_PINOUT_BCM.get('blue_LED_2')),
        }

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
            print('bad LED object passed in v2_gpio.py')