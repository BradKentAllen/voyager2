#!/usr/bin/env python
'''
file name:  brain.py 	#### Modem_Rider
date created:
created by:
project/support: voyager2 Modem_Rider	# root or script it supports
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


class Brain:
	def __init__(self):
		# define gpio_zero objects
		self.blue_LED_1 = LED(config.RPI_PINOUT_BCM.get('blue_LED_1'))

	def LED(self, name, state):
		''' turn LED on or off using name and state
		name: name listed in config.RPI_PINOUT_BCM
		state:  ON or OFF
		'''
		state = state.upper()
		if name == "blue_LED_1":
			if state == "ON":
				self.blue_LED_1.on()
			else:
				self.blue_LED_1.off()
