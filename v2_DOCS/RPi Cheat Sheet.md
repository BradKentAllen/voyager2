# RPi Cheat Sheet



### Basic RPi commands

```
sudo shutdown -h now	# proper way to shut down

sudo reboot  # basic reboot

i2cdetect -y 1	# see all I2C device addresses

sudo python3 my_script.py	# run a python program for RPi gpio

```





### SSH SCP

```
# send files
scp <file_name> raven@45.56.71.57:
scp -r <directory name> raven@45.56.71.57:

# get files
scp raven@45.56.71.57:<file_name> .
scp -r raven@45.56.71.57:<directory name> .

rsync -avP ./RPi_voyager pi@192.168.1.12:

# Host Key Verification Fail
ssh-keygen -R 192.168.1.3

tail -n 500 /var/log/syslog

if __name__ == '__main__':

sudo lsof -i :5000		
kill <PID>
```

### PIP cheat sheet

```
# ### IMPORTANT:  Always use "sudo" in RPi voyager applications.

```

### GPIO

https://embeddedcomputing.com/technology/processing/interface-io/quick-start-raspberry-pi-gpio-terminal-interface

```
raspi-gpio get  # prints the state of all GPIO pins
raspi-gpio get X  # prints the state of GPIO pin X
raspi-gpio set X op  # sets GPIO pin X as an output
raspi-gpio set X dh  # sets GPIO pin X to drive high
raspi-gpio set X dl  # sets GPIO pin X to drive low

# can be combined
raspi-gpio set 10 op dh
```

