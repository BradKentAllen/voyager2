# RPi_voyager Sensors



```
sudo pip3 install Adafruit-Blinka

sudo pip3 install adafruit-circuitpython-adxl34x
sudo pip3 install adafruit-circuitpython-bno055

```





# Sensor Documentation

### Setting Up a Sensor

* Sensors used are defined by the **config.SENSOR_LIST**
* Sensors must have details set up in the **sensor_data_ref** in **resources.py**
* Data is kept in Goop and a sensor is used exclusively to update goop
  * update_sensor_data is a goop method
  * **sensor_mgr must be passed to goop method**
  * 



###### sensor_data_ref parameters (in resources.py)

Name of the sensor (the key in this dict) must be same name as used for the sensor object class

```
'type'		# defines where sensor library/driver comes from
	'voyager' 	# driver is in RPi_voyager
	'blinka'	# uses Adafruit blinka and associated library
	
'data'		# data available from this sensor object 
			# (see sensor data types below)
			
'I2C'		# default I2C address for that sensor
```





### Sensor Data Types

This list includes the availabe data types and the method to get those from a sensor object

```
#### temperature
'temp', 8		# 'F' or 'C'
    <sensor object>.get_temp(update=True, type=<'F'or'C'>, format=True)
'tempF', 8		# 'F'
    <sensor object>.get_temp(update=True, type='F', format=True)
'tempC', 8		# 'C'
    <sensor object>.get_temp(update=True, type='C', format=True)

#### Relative Humidity
'RH', 5			# 'RH' relative humidity usually formatted as integer
    <sensor object>.get_RH(update=True, format=True)

#### Electrical
'V'
'A'

#### Acceleration and Gravity
'acc_X'
'acc_Y'
'acc_Z'

#### Navigation
'latt'
'long'
'bearing'

```







# NOTES





## Circuit Python Drivers

circuit python on RPi with Blinka:  https://www.woolseyworkshop.com/2020/09/29/getting-started-with-circuitpython-on-raspberry-pi-with-blinka/



list of all current Adafruit Circuit Python driver:  https://github.com/adafruit/Adafruit_CircuitPython_Bundle/blob/master/circuitpython_library_list.md



## BNo055

1. Install Blinka:  https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

   ```
   pip3 install Adafruit-Blinka
   ```

   

2. run test program from here:  https://www.woolseyworkshop.com/2020/09/29/getting-started-with-circuitpython-on-raspberry-pi-with-blinka/#InstallingBlinka

   ```
   import board
   import digitalio
   import busio
   print("Hello blinka!")
   # Try to great a Digital input
   pin = digitalio.DigitalInOut(board.D4)
   print("Digital IO ok!")
   # Try to create an I2C device
   i2c = busio.I2C(board.SCL, board.SDA)
   print("I2C ok!")
   # Try to create an SPI device
   spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
   print("SPI ok!")
   print("done!")
   ```

   

3. Run program to make sure it works

4. BNo055:  https://circuitpython.readthedocs.io/projects/bno055/en/latest/

   1. pypi:  https://pypi.org/project/adafruit-circuitpython-bno055/
   2. This site has lots of good detail:  https://gps-pie.com/index.htm
      1. How to do it without changing RPi clock speed.  But this causes problems with other I2C devices:  https://gps-pie.com/pi_i2c_config.htm

5. xx



- clock stretching on RPi:  https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/i2c-clock-stretching

  - this might just be software I2C which could work:  https://github.com/fivdi/i2c-bus/blob/master/doc/raspberry-pi-software-i2c.md

- lots of info in this discussion:  https://forums.adafruit.com/viewtopic.php?f=19&p=774144

- This says RPi4 has clock stretching support:  https://forums.adafruit.com/viewtopic.php?f=19&p=840857

  - The pin layout is identical to earlier versions of the Raspberry Pi and the Pi 4 should be compatible with many hardware add-ons for earlier boards. 

    The Pi 4's GPIO header also supports more connections, with UART, SPI and I2C interfaces each supported on four additional pins, and with fixed [support for clock stretching over I2C interfaces](https://en.wikipedia.org/wiki/I²C#Clock_stretching_using_SCL).