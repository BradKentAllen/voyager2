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

