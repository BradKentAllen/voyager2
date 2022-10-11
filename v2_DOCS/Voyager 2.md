# Voyager 2

gpiozero docs:  https://gpiozero.readthedocs.io/en/stable/



### TODO

- [ ] Shutdown and Reboot
  - [ ] delay while writes to LCD with message on what it is doing
  - [ ] shut down all outputs
  



## Voyager Concept

* All gpio functions are in v2_gpio.py and instantiated as Machine.
  * to use gpio in buttons, pass 'machine' to a button arg in goop, then use
* LCD can be called by a button function by putting the LCD manager into a button_arg in goop 
* XXX_goop must only be instantiated once then sent to other methods.  Otherwise, due to the threading in buttons, there ends up being multiple goops



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

