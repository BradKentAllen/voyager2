# Life Tester A Manual

These instructions augment:

1. Voyager2 guide
2. Voyager_setup guide
3. I2C Devices on Raspberry Pi

### WARNING:  This is not a safety system

Life testers cause machines to operate on their own, operate when no one is present, and drive the machine to failure.  It is inherently hazardous and every test is unique.  As the case with most micro-processor based devices, this life tester is not a safety device and should not be depended on for safe operation and hazard prevention.  A safe program must include:

1. A hazard assessment
2. Physical barriers and signs to prevent people from approaching the life test
3. Mechanical safety devices that will prevent anticipated hazards such as master kill switches, over-temp devices, limit switches, etc.  The hazard assessment should include mitigation for any anticipated hazards.
4. Regular inspections - the test should be stopped and regularly inspected.  The test should be stopped if any failure or progressing pre-failure symptom is detected.  Only after that has been recorded and mitigated should the test be resumed.
5. A ramp up plan where the test is initially run only while observed with more frequent inspections.  Only after the test set up proves itself reliable should it be run over night or on weekends.  Some tests may have inherent hazards that preclude them from being run in an unattended building.



### Overview



### UI

flashing green:  normal operation

two blue:  keyboard interrupt has stopped function

steady red:  main fault, all gpio should be stopped and script should have faulted out

flashing red:  thread fault, all gpio should be stopped but main script is still functioning





### SSH interface

```
ssh tester@192.168.1.6
password:  hawk

# view the log:
tail ./data/log	  # this shows last 10 lines
cat ./data/log	  # this shows the entire file

# modify the stored cycles (modify then save with ctl-X and "Y")
nano ./data/life_cycles

# transfer files
scp LTA_main.py tester@192.168.1.10:
scp sensor_driver.py tester@192.168.1.10:./sensors

```

##### troubleshooting ssh

Permission denied:  if password is correct, verify correct username (e.g. tester) and IP address

connection refused:  this can be caused by several network issues:

* wrong IP address
* verify on same WIFI network
* reboot RPi



### I2C Sensors and Devices

I2C ("eye squared see") is a communication standard for a four-wire bus.  It is designed for using within devices and is thus not effective over long distances without an extender (generally, I2C lines should total less than 3 feet).  Devices are addressed using unique addresses that can sometimes be changed with on-board jumpers (usually soldered).

I2C is powered by either 3.3V or 5V.  The Jim Hawkins board has both available with most sensors being 3.3V and the 5V system used for LCD displays.

Voyager 2 setup has I2C tools loaded by default.  This is a command line set of tools with the most useful being able to check for for what devices are attached.  

```
# view all connected I2C devices
sudo i2cdetect -y 1		# see all I2C devices
```



### Hardware Pinout

On Jim Hawkins Board:

Header 1 (8 pin):

* pin 1:  Ground
* pin 2:  3.3 VDC
* pin 3:  (output 26, jumpered)  Up Relay
* pin 4: (output 15)  Down Relay
* pin 5: (output 18)  up limit switch
* pin 6: (output 23)  down limit switch
* pin 7: (output 24)  not used
* pin 8: (output 21, jumpered)  not used

Header 2 (6 pin):  Buttons

* pin 1:  ground
* pin 2:  3.3 VDC
* pin 3:  (output 12)  button 1 (next screen)
* pin 4:  (output 16) button 2 (right lower)
* pin 5:  (output 20)  button 3 (right upper)
* pin 6:  not used
