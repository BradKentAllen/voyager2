# README

rev Z.0.20



extensive documentation can be found here: XXXXX

dependencies

```
pytz
smbus
gpiozero

#### optional
pigpio
pygame
```



# Troubleshooting

* install Adafruit drivers
* pigpio daeman (sudo systemctl enable pigpiod)



## Install and Run RPi_voyager

###### Step 1:  Install RPi_voyager

* pigpio daeman
* 

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

## Debugging RPi_voyager in your RPi

RPi_voyager contains some debugging tools to help you find errors you may have due to parameters you have set in you my_RPi_config.py (config).  There are two steps you should take to locate errors:

##### Step 1:  Validate your my_RPi_config file

The my_RPi_config file may be validated either using command line and seeing results on the console or during normal execution in which case results will show on the RPi display.

**Debugging on the Console.**  Note that operation will stop with a raised error for each problem found in the my_RPi_config.py file.  Once it is fixed, you can look for the next error.

```
#### To debug while viewing the console, set the following in your my_RPi_config.py file:
VALIDATE_CONFIG = True	# will run a validation on my_RPi_config
DEBUG = True			# will print results on the console, not the RPi display
```

Debugging on the RPi display.  In this mode it will complete the full validation of my_RPi_config.py and display all issues on the LCD.  You can leave this as the default setting in the config if you wish to have the config checked each operation.

```
#### To validate the config on the RPi display:
VALIDATE_CONFIG = True	# will run a validation on my_RPi_config
DEBUG = False			# will show validation results on the RPi display
```



##### Step 2: Debug machine operation

If your my_RPi_config.py file validates but your RPi machine has a run problem, you will need to debug using the console.  To do that:

```
#### Debug through console
DEBUG = True
```

With DEBUG set you get the python exception raised by the problem you are having and may also see additional debug prints from the code.



# READ THE DOCS

XXXX - Link to documentation website goes here