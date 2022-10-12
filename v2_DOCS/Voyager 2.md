# Voyager 2

gpiozero docs:  https://gpiozero.readthedocs.io/en/stable/



### TODO

- [ ] Shutdown and Reboot
  - [ ] delay while writes to LCD with message on what it is doing
  - [ ] shut down all outputs
  



## Voyager Concept

* All gpio functions are in v2_gpio.py and instantiated as Machine.
  * 
* LCD can be called by a button function by putting the LCD manager into a button_arg in goop 
* XXX_goop must only be instantiated once then sent to other methods.  As such, goop is instantiated in the XXX_main.py then sent to other classes later.  Otherwise, due to the threading in buttons, there ends up being multiple goops

### Buttons and Inputs

* Buttons are wired on the Jim Hawkins board with 3.3V pull-ups.  
* Buttons are configured using constants in config:
  * pullup=False is required or test (is pressed) will be reversed.
  * debounce (bounce time) is required for mechanical switches (although not really for push buttons).  A time of .1 seemed best suited for rough mechanical touches
* Buttons can activate functions:
  * when pressed
  * when released
  * when held beyond the hold_time
* Buttons can also be tested with .is_pressed.  This returns True or False.
* Button functions cannot receive parameters.  The following work around allows parameters:
  * buttons can call parameters from goop.  
  * buttonX_args is used for this purpose.
* Machine is passed to XXX_UI so that gpio functions can be called from within a button.  For example, you can directly engage an output.

## Technical

##### self tests

The following modules have self test scripts if run independently:

1. v2_LCD_utility.py
2. 

## Sensors

INA 219 multimeter:  https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/python-circuitpython



#### Circuit Python Drivers

circuit python on RPi with Blinka:  https://www.woolseyworkshop.com/2020/09/29/getting-started-with-circuitpython-on-raspberry-pi-with-blinka/



list of all current Adafruit Circuit Python driver:  https://github.com/adafruit/Adafruit_CircuitPython_Bundle/blob/master/circuitpython_library_list.md

