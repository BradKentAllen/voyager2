# RPi_voyager Documentation

rev Z.0.x

## Install and Run RPi_voyager

###### Step 1:  Install RPi_voyager

XXX

###### Step 2:  Use utility to get machine configuration template

```
# get template
XXXXX

# change name to my_RPi_config.py
cp <machine_name> my_RPi_config.py
```

###### Step 3:  Use utility to get RPi_app.py

```
# get RPi_app.py
XXXXX
```

optional:  you can also create RPi_app.py from scratch:

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RPi_app.py
'''RPi_app.py initiates the app factory in RPi_voyager
Using your my_RPi_config file, RPi_app builds a custom
app to run your Raspberry Pi headless with GPIO.

AditNW LLC, Redmond , WA
www.AditNW.com
'''

__author__ = 'Brad Allen, AditNW LLC'

import signal
from RPi_voyager import create_machine

machine = create_machine()

def keyboardInterruptHandler(signal, frame):
    '''safe handle ctl-c stop'''
    exit(0)

def remote_startUp():
    '''function for call from startUpProgram
    This allows auto start up from a common file
    Can also be called in differentdirectory in RPi'''
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    machine.run()

if __name__ == "__main__":
	# react to keyboard interrupt
    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    machine.run()
```

###### Step 4:  Modify my_RPi_config.py for your configuration

XXXX - how to modify my_RPi_config.py

###### Step XXX:  Run RPi_voyager

IMPORTANT:  RPi_voyager must be run in sudo for access to gpio pins on the Raspberry Pi

```
sudo python3 RPi_app.py
```



## How to Modify my_RPi_config.py

XXXXX



## Configure RPi to run RPI_voyager on startup

XXXX - this section needs customized to docs

##### Run startUpProgram.py at boot

create Start.txt file to be converted to Start.service.  Note User can be pi or root.

```Start.txt
[Unit]
Description=serviceStart
After=network.target

[Service]
ExecStart=/usr/bin/python3 -u startUpProgram.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
User=root

[Install]
WantedBy=multi-user.target
```



```startup
sudo cp Start.txt /etc/systemd/system/Start.service   # copy and rename
sudo systemctl enable Start.service		# enable the startup.
```

##### startUpProgram.py

this requires the function below in the program called (voyager_run.py)

```
# startUpProgram
''' just starts another program '''

import sys

sys.path.insert(1, './voyager')

import voyager_run as startProgram

if __name__ == '__main__':
    startProgram.remote_startUp()
```

Function in main program

```
def remote_startUp():
    '''function for call from startUpProgram in different
    directory in RPi'''
    print('remote start TVcabinet')
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    app = Voyager()
    app.run()
```



## Setting up Raspberry Pi 2, 3, 4 and Zero for RPi_voyager

##### install packages

```
sudo apt-get update && sudo apt-get dist-upgrade -y   # update software
sudo apt install python3-pip		# install pip3

#### Enable I2C in raspi config
sudo raspi-config	# enable I2C

sudo pip3 install smbus		# for LCD (remember must load as sudo)
sudo apt-get install -y i2c-tools	# includes i2c detect
sudo i2cdetec -y 1		# see all I2C devices
sudo apt install python3-gpiozero		# uses RPI.GPIO in more convenient way

```

##### usbmount

RPi_voyager accomodates using an external USB.  To do this, the RPi must have usbmount installed with modifications to support it.  If the usb_mount flag is True in my_RPi_config, on startup the RPi will search for the USB drive and which mount it is on (usb0 to usb7)

discussion on installed usbmountt:  [https://www.raspberrypi.org/forums/viewtopic.php?t=205016](https://www.raspberrypi.org/forums/viewtopic.php?t=205016)

```
#### USB

# install usb mount
sudo apt-get install usbmount

# You must modify a flag in /lib/systemd/system/systemd-udevd.service
# For Rasbian OS Buster and all Raspberry Pi OS versions (including RPi OS Lite):
# Change 
PrivateMounts=yes 
# to 
PrivateMounts=no

sudo nano /lib/systemd/system/systemd-udevd.service   # modify file
# (up to Pi 3 and Stretch):
# Change 
MountFlags=slave 
# to 
MountFlags=shared


```



Note: RPi OS lite seems to have the same flag as this:

different for RPi4 and Buster:  https://raspberrypi.stackexchange.com/questions/100312/raspberry-4-usbmount-not-working

## Appendix:  Package Structure

##### **Dependencies**

smbus
gpiozero
pytz
schedule
pygame



##### Package File Structure

```
├── RPi_app.py
├── my_RPi_config.py
├── startUpProgram.py
│
└── RPi_voyager/
    ├── __init__.py
    ├── mechanic.py
    ├── resources.py
    ├── UI.py
    ├── logger.py
	│
	├── README.txt
	│
	├── machines/
	│   ├── alarm_clock.py
	│   └── rpi_utilities.py
	├── displays/
	│   ├── __init__.py
	│   ├── LCD_I2C.py
	│   ├── LCD_wired.py
	│   ├── LCD.fake.py
	│   └── XXXX.py
	├── outputs/
	│   ├── __init__.py
	│   └── XXXX.py
	├── XXXX/
	│   ├── XXX.py
	│   └── XXXX.py


├── .gitignore
├── LICENSE
├── requirements.txt
├── LIBRARY
│   ├── RPi_app.py
│   ├── machine config files
│   ├── voyager_file_utility.py
│   └── XXXX.py
└── setup.py
├── tests/
	│   ├── helloworld_tests.py
	│   └── helpers_tests.py
```

