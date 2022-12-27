# I2C Device on Raspberry Pi

Most I2C sensors require some sort of interface or driver package.  On RPi, it is usually easier to use a .py file that you download.  It is convenient to build a self-test into the package so if it is run independently it will test the sensor.

### I2C Addresses

```
LCD					0x27  # can be changed with jumper to 0x23
HIH6121				0x27  #fixed
BNo055				0x28
ADS1115 (A to D)	0x48  # requires ads1115driver.py
ADXL345				0x53
DS1307 RTC			0x68 (will show as UU)
BNo055 (compass)	0x69
Ultimate GPS
```



## Working with I2C Devices

```
# view all connected I2C devices
sudo i2cdetect -y 1		# see all I2C devices
```





## Using 5V I2C devices on Raspberry Pi

Although your Raspberry Pi is powered by 5 VDC and has that available, its logic voltage is 3.3 VDC.  If a 5V device is powered by 5 VDC then connected to your RPi's I/O, such as pins 2 and 3 for I2C, you will risk damaging your RPi.  This limits what devices you can use.

One 5 volt device that is very convenient to use are the many inexpensive 16x2 and 20x4 LCD displays with I2C communications.  These displays are easy to use and bright enough to be easily readable outdoors even in the sun.  Although you may successfully use them at 3.3 volts, they also have problems with this low voltage.  The answer is a simple level shifting circuit between the 3.3v and 5v portion of the I2C bus.

### Off the shelf Level Shifter

Adafruit makes a nice level shifting breakout board to perform this function:  https://www.adafruit.com/product/757



### DIY Level Shifter

It's pretty simple to build your own level shifter with only 6 components.

* (qty 2) 2N7000 FET NPN transistors
* (qty 4) 4.7k resistors

<img src="../static/markdown_images/2n7000-pinout.gif" alt="drawing" width="50%"/> 

![level_shifter_schematic](../static/markdown_images/level_shifter_schematic.png)

