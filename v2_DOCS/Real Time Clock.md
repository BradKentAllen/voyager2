# Real Time Clock

how to add:  https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time

### Step 1:  Add dtoverlay to /boot/config.txt

```
sudo nano /boot/config.txt

# add one of these to the last line of config.txt
dtoverlay=i2c-rtc,ds1307
dtoverlay=i2c-rtc,ds3231
dtoverlay=i2c-rtc,pcf8523
```

### Step 2:  Verify RTC is running

```
# reboot
# check for UU in i2cdetect

sudo i2cdetect -y 1
```



### Step 3:  Disable the 'fake hwclock'

```
sudo apt-get update
sudo apt-get -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
sudo systemctl disable fake-hwclock

# if fake-hwclock is masked:
sudo systemctl unmask fake-hwclock

# view all services and status
systemctl --type=service
```



### Step 4:  Modify the hwclock-set routine

```
sudo nano /lib/udev/hwclock-set
#### comment out these lines:
#if [ -e /run/systemd/system ] ; then
# exit 0
#fi

#### and comment out these lines (note these are in the if and the else):
#/sbin/hwclock --rtc=$dev --systz --badyear
#/sbin/hwclock --rtc=$dev --systz
```



### Step 5:  Test and Set the Hardware Clock (RTC)

```
# get the current time and date
date

# read the hardware clock:
hwclock -r

# if this does not work, try
sudo hwclock -r

# write the time to the hardware clock:
hwclock -w
```



### Get hwclock from python

```python
import os

os.system("sudo hwclock -r")
```



### Troubleshoot hwclock

```
sudo -s		# this does super user without environmental variables ("exit" will leave this mode)
hwclock -r
```

