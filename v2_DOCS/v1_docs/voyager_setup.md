



# Voyager - Setup



#### TODO

* headless has a boot problem without hdmi.  

```
#### uncomment or add this to /boot/config.txt
hdmi_force_hotplug=1
```







How to set up a Raspberry Pi for use with RPi_voyager.

## Getting Started

We use a common setup approach to all RPi_voyager machines.  This is an attempt to reduce problems later on.  Raspberry Pi's are versatile machines and can be set up in a variety of ways.  This is just one.  But, if you follow this setup it is much easier to troubeshoot using our instructions.

On operating systems:  RPi_voyager is optimized for use with the standard Raspberry Pi OS.  SD cards are reasonably inexpensive so it is easy to have a minimum 16GB micro SD card that easily accomodates Raspberry Pi OS.  With full Raspberry Pi OS installed you can run "headless" (without a screen, monitor, and keyboard) but always have the option to use them for troubleshooting.

Why not Raspberry Pi OS lite? - Raspberry Lite is useful in memory constrained machines.  In order to accomplish this a variety of standard software is not included.  This includes software key to the RPi_voyager schema such as drivers for USB drives.

### Step 1:  Format SD card

1. **SD Card**:  Start with a high quality SD card such as the SanDisk Ultra.  It is a false savings to use an old, off-brand, or questionable SD card.  A minimum 16GB card is recommended.  For more on card requirements: https://www.raspberrypi.org/documentation/installation/sd-cards.md

![Sandisc_ultra](../static/markdown_images/Sandisc_ultra.jpg)

2. **Format the SD Card**:  It is a good idea, although not mandatory, to format your SD card first.  Do not use the utilities in your PC or laptop.  Use a high-quality tool such as SD Card Formatter: https://www.sdcard.org/downloads/formatter/
3. **Install Raspberry Pi OS**:  The Raspberry Pi Imager is the official method to install the operating system on the SD card.  It is simple and free.  Use this link for download and instructions:  https://www.raspberrypi.org/software/ .  Key steps after downloading the Raspberry Pi OS image tool:
   * **Choose OS**:  Select the Raspberry Pi OS (32 bit) - this the default option
   * **Select your SD card**.
   * **Write**



### Step 2: Set up with Monitor, Keyboard, and Mouse

1. Insert SD card, connect monitor, keyboard, and mouse
2. Turn power on and follow instructions to set up
3. 

```
#### get network info
ifconfig	# this will give you your IP address
```



### Step 3:  Update Key Settings

By default, your RPi will boot up with a username of 'pi' and a hostname of raspberrypi.  It is a good idea to change the hostname to uniquely identify your machine.  We recommend keeping the user as 'pi' to maintain the default filestructure and permissions.

##### Using raspi-config

open a terminal window by clicking the small black box in the top bar:

```
# enter raspi-config:
sudo raspi-config

# follow instructions to do the following:
1.  Change hostname   (1 System Options - S4 Hostname)
2.  Enable key interfaces (3 Interface Options) then do the following:
	P2 SSH
	P5 I2C
	
	P1 camera (only if you intend to use a camera)
	
# follow the instructions to reboot if you changed the hostname
	
```



```
sudo nano /etc/hostname		# file only contains the hostname, change it and 
							save (ctl-X then Yes)
sudo nano /etc/hosts		# last line is host name, change it and save
```



### Step 4:  Install Software

You will be installing various software libraries required for RPi_voyager.  The following is all done in terminal.  

note on sudo:  As RPi_voyager is intended for standalone machines, all software is installed at the root permission level using sudo ('super user do').  This is especially important as the input output requires root (super user) access.

```
# update the Ubuntu software list
sudo apt-get update

# update all Ununtu software
sudo apt-get dist-upgrade -y

# verify the python3 install tool is available:
pip3 list

# if not, install the python3 install tool pip
sudo apt install python3-pip

# use the list from pip3 list to check for the following software, install if not there
gpiozero	# to install:  sudo pip3 install python3-gpiozero

# the following software is most likely not there and needs installed:
sudo pip3 install smbus
sudo pip3 install pytz
sudo apt-get install -y i2c-tools

# with some machines we will use pigpio (primarily for machines with servos).  You will need to enable a daemon for this to run:
sudo systemctl enable pigpiod

```



# install RPi_voyager package

XXXX - GitHub????



# Test RPI_voyager is working

XXXX - design a simple test program (e.g. alarm_clock style)

# Set up auto start on boot up

RPi_voyager is primarily intended for machines running autonomously and, as such, need to start their programs on boot.  To accomplish that, we will use the systemd package included with Raspbery Pi OS.  Using systemd, we can set up a 'service' that will start on boot.  The steps are:

1. Add a startUpProgram.py that calls the program you wish to start.  This is not required but allows you to easily change what program you want to start without using the systemctl.  (note: if you choose to start a program other than RPi_app.py, you will need to modify startUpProgram.py and add some code to your program.  See XXXXADD LINK Services and systemctl for more details)
2. Create a service (script) that systemctl uses at boot to call the startUpProgram.  
3. enable the system to run at boot

Once you have done this, there are some things to keep in mind:

* When you restart your RPi, the service will be running.  If you wish to do tests, such as starting and stopping the program over ssh, you will need to stop the service.
* If you observe odd behavior, such as displays not running correctly or outputs misbehaving, check if you inadvertantly are running two programs.  For example, Start.service has RPi_voyager running and you have manually started it on command line or over ssh.
* Common systemctl commands you will find useful:

```
sudo systemctl start Start.service	# starts the service, calls the program, but does not enable it for start at boot

sudo systemctl stop Start.service	# stops the service

sudo systemctl status Start.service	# shows if service is running and any errors that occured in startup.

sudo systemctl enable Start.service		# enables your service to start on boot

sudo systemctl disable Start.service	# disables auto start
```

### Set up auto start

##### Step 1:  Verify you have startUpProgram.py

You must have startUpProgram.py in your /home/pi directory for this to work.  If it is not there:

XXXX How to get startUpProgram.py

**Step 2: Set up Start.service**

On command line, create Start.service: 

```
sudo nano /etc/systemd/system/Start.service		# opens the nano text editor and creates service at that location
```

Copy the following code into the nano editor.  Then save (ctl X, then confirm with 'Y' for yes)

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

Note some important things going on in this service:

* ExecStart:  It is calling the program startUpProgram.py using python3
* WorkingDirectory:  note this
* User:  by designating user as "root" you give full root permission to the program call (equivalent to sudo python3).  This is required for the RPi to effectively call inputs and outputs under the RPi_voyager schema.

It is a wise idea to test that your service is working.  To test:

```
sudo systemctl start Start.service		# this will run the program

sudo systemctl status Start.service		# verify it is running without errors
```

Finally, enable the service to run at boot:

```startup
sudo systemctl enable Start.service		# enable the startup.
```

For more depth on how this works, see XXXXADD LINK Services and systemctl

### XXX - Copied, not reviewd

### WIFI

WIFI credentials are contained in this file:

wpa_supplicant.conf ends up here:   /etc/wpa_supplicant/wpa_supplicant.conf

```wpa supplicant
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="network name"
scan_ssid=1
psk="password"
key_mgmt=WPA-PSK
}
```

```

```







### Change RPi name (hostname):

```


passwd						# change password
```







### Tracking Your Configurations



```
name:
Board: Raspberry Pi 4
hostname: raspberry
user: pi
password:  <my password>
fixed IP: 
card:  Full Raspbian OS
```

 