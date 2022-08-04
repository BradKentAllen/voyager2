# Services and systemctl



##### Run startUpProgram.py at boot

To start a program at startup you need:

1. A service in systemctl that calls the program (and which also must be enabled)
2. code within the program to start
   * in RPi_voyager there is an extra step:
     * the service is Start.service
     * Start.service calls startUpProgram.py
     * RPi_app.py requires some code to start

### systemctl commands

RPi_voyager uses the following services.  You will have set them up as part of the setup:

Start.service			Runs RPi_voyager on boot

pigpiod					This is a daemon required by pigpio.

uwsgi.service		Starts the uwsgi and nginx server at boot (voyager_server setup only)

```
sudo systemctl start Start.service	# start service in current session
sudo systemctl stop Start.service	# stop service in current session
sudo systemctl status Start.service # see if service is running with some errors

sudo systemctl enable Start.service	# enable service to run at boot
sudo systemctl disable Start.service	# disable service from running at boot
```



### create Start.service 

```
sudo nano /etc/systemd/system/Start.service
```

Start.service:

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
sudo systemctl enable Start.service		# enable the startup.
```

##### 

### create startUpProgram.py

Make sure startUpProgram.py is in /home/pi

this requires the function below in the program called (voyager_run.py)

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# startUpProgram.py
'''startUpProgram makes it easy to set up RPi to
automatically start your machine on boot.  By 
calling startUpProgram, you can start any program.
Note how you can uncomment lines to reach into a 
directory.

AditNW LLC, Redmond , WA
www.AditNW.com
'''

#### uncomment these two lines to start a program
# in a directory
#import sys
#sys.path.insert(1, './<directory>)

import RPi_app as startProgram

if __name__ == '__main__':
    startProgram.remote_startUp()
```



### Assure proper code is in the called program (RPi_app.py)

The following code must be in RPi_app.py

```
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



