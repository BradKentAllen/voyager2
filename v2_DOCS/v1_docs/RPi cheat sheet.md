

# Raspberry Pi Cheat Sheet



## Common Tasks

```
sudo reboot
sudo shutdown -h now


```



### ssh, scp, rsync

```
#### ssh gives you command line control of your RPi
ssh pi@192.168.1.13

# Transfer a file (scp, secure copy, can copy files to or from your RPi)
scp my_file.py pi@192.168.1.13:

#### transfer a package
# using ssh, delete a directory and its contents:
rm -r RPi_voyager

# scp a directory and its contents
scp -r RPi_voyager pi@192.168.1.18:

#### scp from RPi to your computer (these commands at receiving computer)
scp pi@192.168.1.11:filename.py .   # from RPI (NOTICE THE SPACE & DOT)
scp pi@192.168.1.11:directory/filename.py .   # Yep, the DOT & SPACE 

#### rsync will syncronize all files and folders in a directory
# use rsync
rsync -avP ./RPi_voyager pi@192.168.1.12:

# -a copies all recursively with permissions (it replaces -r)
# -P gives progress and will resynch if interrupted
# -v is verbose
```



### RPi using ethernet

https://medium.com/@tzhenghao/how-to-ssh-into-your-raspberry-pi-with-a-mac-and-ethernet-cable-636a197d055

troubleshoot:

https://discussions.apple.com/thread/4274865

```
ping <host_name>.local
ssh <host_name>.local
ssh raspberrypi.local
ssh fred.local
```



# Managing SD Cards

https://www.raspberrypi.org/documentation/linux/filesystem/backup.md

RPi OS has an SD card copier

```
#### on computer:
sudo dd bs=4M if=/dev/sdb of=PiOS.img	# save an SD card image to drive 
sudo dd bs=4M if=PiOS.img of=/dev/sdb	# clones from drive to SD card
```





# Troubleshooting

```
sudo i2cdetect -y 1		# lists all I2C connected devices (remember you must reboot to find an I2C device)
```



### Headless Troubleshooting

With autostart:

```
sudo systemctl start Start.service	# starts the service, calls the program, but does not enable it for start at boot

sudo systemctl stop Start.service	# stops the service

sudo systemctl status Start.service	# shows if service is running and any errors that occured in startup.

sudo systemctl enable Start.service		# enables your service to start on boot

sudo systemctl disable Start.service	# disables auto start
```

### 

##### Won't Boot

```
# Are you using a power supply with at least 2.5 Amps at 5.2 Volts?
# On a new board the country must be set.  This will require a keyboard and monitor

```



##### Host Key Verification Failed:

"Host key verification failed" means that the host key of the remote host was changed.  This typically happens when your wifi assigns an IP address to your RPi that you have used in the past.  It is a good security feature, but you have to bypass it in this situation.  This command is entered on your computer to reset the ssh hostly.

```host key verification failed
ssh-keygen -R 192.168.1.3    #directly removes offending file
```



### Wifi troubleshooting

* check for wpa_supplicant (/etc/wpa_supplicant/wpa_supplicant.conf)
* check location and timezone are correctly set (sudo raps-config)

```
sudo raspi-config
localization
L4 WLAN country		# note: do not mess with L1 Locale
L2 Timezone
```

```
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









# OLD MATERIAL - REVIEW



##### Available Memory

check usage:  https://learn.adafruit.com/an-illustrated-shell-command-primer/checking-file-space-usage-du-and-df

```
du -hs	# disk used
df -h	# disk free
free -h		# RAM free
```

Expand file system with larger card

```
sudo raspi-config
7. Advanced Options
A1 Expand Filesystem
reboot
```

##### Direct connect RPis Zero with USB

Good article:  https://www.muo.com/tag/directly-connect-raspberry-pi-without-internet/

This seems to be the process:  https://gist.github.com/gbaman/975e2db164b3ca2b51ae11e45e8fd40a

Some details here:  https://www.circuitbasics.com/raspberry-pi-zero-ethernet-gadget/



##### Permissions

modify this file to not require sudo password:

/etc/sudoers.d/010_pi-nopasswd

```
/etc/sudoers.d/010_pi-nopasswd		# file controls sudo password

# only has a single line
pi ALL=(ALL) NOPASSWD: ALL

# change user
raven ALL=(ALL) NOPASSWD: ALL

# require password
pi ALL=(ALL) PASSWD: ALL
```



##### Remote access

```
ssh pi@192.168.1.11					# connect to user pi
scp filename.py pi@192.168.1.11: 	# transfer to home directory
scp filename.py pi@192.168.1.11:directory/	# into this directory in home/pi


```

##### Install Issues

problems with statsmodels

```
sudo apt-get update
sudo apt-get install libatlas-base-dev	# required for numpy

# remember to use sudo on flask RPi
pip3 install statsmodels		#(let statsmodels install these dependencies:  numpy 1.18.1, pandas 1.0.1, scipy 1.4.1, Patsy 0.5.1)
pip3 install bokeh		# (ipython was already on RPi)
# matplotlib was already on RPi
```





##### startUpProgram

```
import sys

sys.path.insert(1, './TVcabinet')

# TV_runner is the actual RPi python app
import TV_runner as startProgram

if __name__ == '__main__':
    startProgram.remote_startUp()
```



this is the actual program:

```
def keyboardInterruptHandler(signal, frame):
    '''safe handle ctl-c stop'''
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    GPIO.cleanup()
    exit(0)


def remote_startUp():
    '''function for call from startUpProgram in different
    directory in RPi'''
    print('remote start TVcabinet')
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    data = ProgramData()  # only object just called 'data'
    app = TVcabinet(data)


if __name__ == '__main__':
    print('start')
    # react to keyboard interrupt
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    data = ProgramData()  # only object just called 'data'
    app = TVcabinet(data)
    # shut off GPIO and shutdown 
    GPIO.cleanup()

    print('end script')
```



 



* Find .ssh file:
    * cd ~/.ssh
    * ls to show files
    * nano to edit



Remote Control


Transfer a file default to home/pi :  scp fileName.py  pi@192.168.1.11:
https://www.raspberrypi.org/documentation/remote-access/ssh/scp.md

Stop all python:  sudo killall python3

Power off:  sudo shutdown -h now
Reboot:  sudo reboot

scp weather.py pi@192.168.1.12:WEATHER/
head -20 weather.py


Remote control a python3 program through ssh:
* Use systemctl:  https://www.raspberrypi.org/documentation/linux/usage/systemd.md
* RTC commands
    * Check status of all clocks:  timedatectl status
    * Set RTC:  sudo hwclock --set --date="2011-08-14 16:45:05"
    * Set RPI to RTC time:  sudo hwclock -s
    * Set RTC to RPI time:  sudo hwclock -w
    * Read the RTC time (not RPI):  sudo hwclock -r

Industrial RPi
balenaFin is great looking product:  https://store.balena.io/collections/frontpage

##### **Backup Disc/Disk Image**

1. Insert card in Mac
2. Disc utility
3. Select the device (not ‘Boot’, might have to do View-Show Devices to see)
4. File - New Image - Image from <device name>
5. Select ‘DVD/CD master’ from the format drop down in bottom right of file popup
6. This should create a .cdr file

NOTE:  if you get an error here on Mac:

Prefs -> Security & Privacy -> Privacy tab -> Full Disk Access (in list on left side of window)

Click on the lock at the bottom left of the screen, enter your password, then press the + button near the centre of the screen. Add Disk Utility to the list. Click on the lock again and things should work.

###### Restore an image:

1. Change file extension to .iso
2. Format new disc using SD Formatter
3. Use Etcher to flash this image to the new disc

* 

##### Checking logs, startup and system commands

* Get system log (this is for 2000 lines):  tail -n 2000 /var/log/syslog
* Get list of services:  sudo systemctl list-unit-files
* Get list of enabled services:  sudo systemctl list-unit-files | grep enabled

![syslog settings](../noteImages/syslog settings.png)



##### GPIO

* Cleanup outputs (when have used output).  This changes all outputs to inputs:  GPIO.cleanup()
    * http://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi


GENERAL COMMANDS
* apt-get update: Synchronizes the list of packages on your system to the list in the repositories. Use it before installing new packages to make sure you are installing the latest version.
* apt-get upgrade: Upgrades all of the software packages you have installed.
* clear: Clears previously run commands and text from the terminal screen.
* date: Prints the current date.
* find / -name example.txt: Searches the whole system for the file example.txt and outputs a list of all directories that contain the file.
* nano example.txt: Opens the file example.txt in the Linux text editor Nano.
* poweroff: To shutdown immediately.
* raspi-config: Opens the configuration settings menu.
* reboot: To reboot immediately.
* shutdown -h now: To shutdown immediately.
* shutdown -h 01:22: To shutdown at 1:22 AM.
* startx: Opens the GUI (Graphical User Interface).
* umount (sudo umount /media/usb0)



##### FILE AND DIRECTORY COMMANDS

* stat - file information/data
* ls -la    returns files, folders, and permissions
    * example:  drwx-xr-x
    * first character is:
        * -  file
        * d  directory
        * l  link
    * then has 3 groups
        * owner
        * group
        * users
    * permissions are:
        * r    read
        * w   w
        * x    execute
    * chmod +rwx fileName
        * + or - for add or delete permission
        * then the permissions
* 
* cat example.txt: Displays the contents of the file example.txt.
* cd /abc/xyz: Changes the current directory to the /abc/xyz directory.
* cp XXX: Copies the file or directory XXX and pastes it to a specified location; i.e. cp examplefile.txt /home/pi/office/ copies examplefile.txt in the current directory and pastes it into the /home/pi/ directory. If the file is not in the current directory, add the path of the file’s location (i.e. cp /home/pi/documents/examplefile.txt /home/pi/office/ copies the file from the documents directory to the office directory).
* ls -l: Lists files in the current directory, along with file size, date modified, and permissions.
* mkdir example_directory: Creates a new directory named example_directory inside the current directory.
* Rename:  use mv:   mv oldName newName
* mv XXX: Moves the file or directory named XXX to a specified location. For example, mv examplefile.txt /home/pi/office/ moves examplefile.txt in the current directory to the /home/pi/office directory. If the file is not in the current directory, add the path of the file’s location (i.e. cp /home/pi/documents/examplefile.txt /home/pi/office/ moves the file from the documents directory to the office directory). This command can also be used to rename files (but only within the same directory). For example, mv examplefile.txt newfile.txt renames examplefile.txt to newfile.txt, and keeps it in the same directory.
* rm example.txt: Deletes the file example.txt.
* rmdir example_directory: Deletes the directory example_directory (only if it is empty).
* rm -rf directoryName (for directory with files)
* scp user@10.0.0.32:/some/path/file.txt: Copies a file over SSH. Can be used to download a file from a PC to the Raspberry Pi. user@10.0.0.32 is the username and local IP address of the PC, and /some/path/file.txt is the path and file name of the file on the PC.


NETWORKING AND INTERNET COMMANDS
* ifconfig: To check the status of the wireless connection you are using  (to see if wlan0 has acquired an IP address).
* iwconfig: To check which network the wireless adapter is using.
* iwlist wlan0 scan: Prints a list of the currently available wireless networks.
* iwlist wlan0 scan | grep ESSID: Use grep along with the name of a field to list only the fields you need (for example to just list the ESSIDs).
* nmap: Scans your network and lists connected devices, port number, protocol, state (open or closed) operating system, MAC addresses, and other information.
* ping: Tests connectivity between two devices connected on a network. For example, ping 10.0.0.32 will send a packet to the device at IP 10.0.0.32 and wait for a response. It also works with website addresses.
* wget http://www.website.com/example.txt: Downloads the file example.txt from the web and saves it to the current directory.
SYSTEM INFORMATION COMMANDS
* cat /proc/meminfo: Shows details about your memory.
* cat /proc/partitions: Shows the size and number of partitions on your SD card or hard drive.
* cat /proc/version: Shows you which version of the Raspberry Pi you are using.
* df -h: Shows information about the available disk space.
* df /: Shows how much free disk space is available.
* dpkg – –get–selections | grep XXX: Shows all of the installed packages that are related to XXX.
* dpkg – –get–selections: Shows all of your installed packages.
* free: Shows how much free memory is available.
* hostname -I: Shows the IP address of your Raspberry Pi.
* lsusb: Lists USB hardware connected to your Raspberry Pi.
* UP key: Pressing the UP key will print the last command entered into the command prompt. This is a quick way to repeat previous commands or make corrections to commands.
* vcgencmd measure_temp: Shows the temperature of the CPU.
* vcgencmd get_mem arm && vcgencmd get_mem gpu: Shows the memory split between the CPU and GPU.





##### Clean up the OS

1. Start with Raspbian
2. Delete Libre Office
    1. sudo apt-get remove --purge libreoffice-*
    2. sudo apt-get remove --purge wolfram-engine
    3. If you want to re-install Libre Office:  sudo apt-get install libreoffice wolfram-engine 
3. Clean out cache of downloaded packages: 
sudo apt-get clean 
File Commands
cat <fileName>
Head -20 <fileName>     — first 20 lines of file

##### GENERAL COMMANDS

* apt-get update: Synchronizes the list of packages on your system to the list in the repositories. Use it before installing new packages to make sure you are installing the latest version. 
* apt-get upgrade: Upgrades all of the software packages you have installed.
* cat - view contents (more:  https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/4/html/Step_by_Step_Guide/s1-viewingtext-terminal.html ) 
* clear: Clears previously run commands and text from the terminal screen. 
* date: Prints the current date. 
* find / -name example.txt: Searches the whole system for the file example.txt and outputs a list of all directories that contain the file. 
* nano example.txt: Opens the file example.txt in the Linux text editor Nano. 
* poweroff: To shutdown immediately. 
* raspi-config: Opens the configuration settings menu. 
* reboot: To reboot immediately. 
* shutdown -h now: To shutdown immediately. 
* shutdown -h 01:22: To shutdown at 1:22 AM. 
* startx: Opens the GUI (Graphical User Interface). 

  ##### FILE AND DIRECTORY COMMANDS
* cat example.txt: Displays the contents of the file example.txt.
* cd /abc/xyz: Changes the current directory to the /abc/xyz directory.
* cp XXX: Copies the file or directory XXX and pastes it to a specified location; i.e. cp examplefile.txt /home/pi/office/ copies examplefile.txt in the current directory and pastes it into the /home/pi/ directory. If the file is not in the current directory, add the path of the file’s location (i.e. cp /home/pi/documents/examplefile.txt /home/pi/office/ copies the file from the documents directory to the office directory).
* ls -l: Lists files in the current directory, along with file size, date modified, and permissions. 
* kdir example_directory: Creates a new directory named example_directory inside the current directory.
* mv XXX: Moves the file or directory named XXX to a specified location. For example, mv examplefile.txt /home/pi/office/ moves examplefile.txt in the current directory to the /home/pi/office directory. If the file is not in the current directory, add the path of the file’s location (i.e. cp /home/pi/documents/examplefile.txt /home/pi/office/ moves the file from the documents directory to the office directory). This command can also be used to rename files (but only within the same directory). For example, mv examplefile.txt newfile.txt renames examplefile.txt to newfile.txt, and keeps it in the same directory.
* rm example.txt: Deletes the file example.txt.
* rmdir example_directory: Deletes the directory example_directory (only if it is empty).
* scp user@10.0.0.32:/some/path/file.txt: Copies a file over SSH. Can be used to download a file from a PC to the Raspberry Pi. user@10.0.0.32 is the username and local IP address of the PC, and /some/path/file.txt is the path and file name of the file on the PC.
* stat - gets data on a file
* touch example.txt: Creates a new, empty file named example.txt in the current directory. 
NETWORKING AND INTERNET COMMANDS
* ifconfig: To check the status of the wireless connection you are using  (to see if wlan0 has acquired an IP address). 
* iwconfig: To check which network the wireless adapter is using. 
* iwlist wlan0 scan: Prints a list of the currently available wireless networks. 
* iwlist wlan0 scan | grep ESSID: Use grep along with the name of a field to list only the fields you need (for example to just list the ESSIDs). 
* nmap: Scans your network and lists connected devices, port number, protocol, state (open or closed) operating system, MAC addresses, and other information. 
* ping: Tests connectivity between two devices connected on a network. For example, ping 10.0.0.32 will send a packet to the device at IP 10.0.0.32 and wait for a response. It also works with website addresses. 
* wget http://www.website.com/example.txt: Downloads the file example.txt from the web and saves it to the current directory. 
SYSTEM INFORMATION COMMANDS
* cat /proc/meminfo: Shows details about your memory. 
* cat /proc/partitions: Shows the size and number of partitions on your SD card or hard drive. 
* cat /proc/version: Shows you which version of the Raspberry Pi you are using. 
* df -h: Shows information about the available disk space. 
* df /: Shows how much free disk space is available. 
* dpkg – –get–selections | grep XXX: Shows all of the installed packages that are related to XXX. 
* dpkg – –get–selections: Shows all of your installed packages. 
* free: Shows how much free memory is available. 
* hostname -I: Shows the IP address of your Raspberry Pi. 
* lsusb: Lists USB hardware connected to your Raspberry Pi. 
* UP key: Pressing the UP key will print the last command entered into the command prompt. This is a quick way to repeat previous commands or make corrections to commands. 
* vcgencmd measure_temp: Shows the temperature of the CPU. 
* vcgencmd get_mem arm && vcgencmd get_mem gpu: Shows the memory split between the CPU and GPU.
