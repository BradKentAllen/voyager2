# Voyager 2

ROS:  https://wiki.ros.org

https://yoraish.com/2021/09/08/a-full-autonomous-stack-a-tutorial-ros-raspberry-pi-arduino-slam/

gpiozero docs:  https://gpiozero.readthedocs.io/en/stable/



### TODO

- [ ] switch message to Twillio
  - [ ] write and test weather.



## Voyager Concept

##### 

* read_xxx    -  a sensor
* set_xxx       - this is an output such as a servo or LED

Initiate class objects

1. Goop - data class with all data
   * 
2. Brain
   1. sensor objects
3. LCD_manager (UI.py)
   1. instantiate LCD
   2. methods for display, writing, clear, etc.



## Technical



##### install packages

```
sudo apt-get update && sudo apt-get dist-upgrade -y   # update software
sudo apt install python3-pip		# install pip3

#### Enable I2C in raspi config
sudo raspi-config	# enable I2C

pip3 install pip --upgrade
pip3 install pip-tools

sudo pip3 install smbus		# for LCD (remember must load as sudo)
sudo apt-get install -y i2c-tools	# includes i2c detect
sudo i2cdetec -y 1		# see all I2C devices
sudo pip3 install gpiozero		# uses RPI.GPIO in more convenient way
sudo pip3 install pigpio

```

Startup

Timing Loop

```python
from datetime import datetime
from time import time, sleep
import pytz

while True:
    milli = (time() * 1000) - start_milli
    
    #### set up last varables
    (last_hour, last_minute, last_second) = get_time(self.local_time_zone)
    last_milli = 0
    start_milli = time() * 1000

	#### update milli
    milli = (time() * 1000) - start_milli
    
def get_time_stamp(local_time_zone='UTC', time_format='HMS'):
    now_local = datetime.now(pytz.timezone(local_time_zone))
    if time_format == 'YMD:HM':
        return now_local.strftime('%Y-%m-%d' + '-' + '%H:%M')
    else:
        return now_local.strftime('%H:%M:%S')

def get_time(local_time_zone='UTC'):
    now_local = datetime.now(pytz.timezone(local_time_zone))
    HH = now_local.strftime('%H')
    MM = now_local.strftime('%M')
    SS = now_local.strftime('%S')
    return (HH, MM, SS)
```



Utility functions 

* display (use LCD_manager)



## Sensors

INA 219 multimeter:  https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/python-circuitpython



#### Circuit Python Drivers

circuit python on RPi with Blinka:  https://www.woolseyworkshop.com/2020/09/29/getting-started-with-circuitpython-on-raspberry-pi-with-blinka/



list of all current Adafruit Circuit Python driver:  https://github.com/adafruit/Adafruit_CircuitPython_Bundle/blob/master/circuitpython_library_list.md

