# NomiNomi



home IP:  192.168.1.220

Pass:  goose13



##### wpa_supplicant for WIFI

looks for mobile WIFI first then AllenNet1

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
	ssid="Raven_Nest"
	psk="goose133"
	key_mgmt=WPA-PSK
}

network={
	ssid="AllenNet1"
	psk="fiGure8knot87881?"
}
```



## Operations Notes

* Boat needs to point generally North on power up
* Wiggle boat during and after power up to engage compass
* Boat needs to be pointed into a sail-able wind angle when START is pressed.  It will intially sail this course until a distance from home.

#### Standards and Definitions

* Heel
  * heel to starboard is positive (on a port tack, heel will be positive)
  * heel to port negative
* Rudder
  * rudder steer to starboard is positive (rudder turned to starboard)
* Heading
  * heading_compass - compass direct reading
  * heading_boat - heading_compass compensated for declination and other corrections
  * heading_course - heading to next waypoint (nav_leg direction)
  * heading_differential = heading_boat - heading_course
    * a positive heading_differential requires steering to starboard, this is a positive rudder
* Nav Units
  * 69 miles in one degree of lattitude
  * at 45 deg lattitude, one degree of longitude is 41 miles
  * 1 knot = 1.7 ft/sec
  * 5 sec at 1 knot = 8.5 ft

## Hardware Technical Notes

```
# Aug 2022 list
LCD					0x23
BNo055				0x28
ADC (wind/volt)		0x48
ADXL345				0x53
DS1307 RTC			0x68 (will show as UU)
BNo055 (compass)	0x69
Ultimate GPS

# ### OLD

LCD				0x23
ADC (wind/volt)	0x49	
servo board		0x40
9-axis accel	0x69 (or 0x68)
```

#### Compass

https://peppe8o.com/magnetometer-with-raspberry-pi-computers-gy-271-hmc5883l-wiring-and-code/

for yacht:  https://www.roboticboat.uk/Microcontrollers/RaspberryPi3/CMPS14/CMPS14.html

## Software Technical Notes

- GPS
    - When there is no fix, the FIX pin and Red LED  pulse up and down once every second. When there is a fix, the pin is low (0V) for most of the time, once every 15 seconds it will pulse high for 200 milliseconds
    - GPS returns NMEA in format DDMM.MMMM but the circuit python library parses this to **decimal degrees**.
    - Haversine:  https://pypi.org/project/haversine/
    - angle:  https://towardsdatascience.com/calculating-the-bearing-between-two-geospatial-coordinates-66203f57e4b4
    - Ultimate GPS:  https://learn.adafruit.com/adafruit-ultimate-gps/circuitpython-parsing



#### installed libraries

```
Adafruit-Blinka                  6.4.0
adafruit-circuitpython-adxl34x   1.12.6
adafruit-circuitpython-bno055    5.2.5
adafruit-circuitpython-busdevice 5.0.6
adafruit-circuitpython-gps       3.8.0
adafruit-circuitpython-register  1.9.5
Adafruit-PlatformDetect          3.3.0
Adafruit-PureIO                  1.1.8
asn1crypto                       0.24.0
astroid                          2.1.0
asttokens                        1.1.13
automationhat                    0.2.0
beautifulsoup4                   4.7.1
blinker                          1.4
blinkt                           0.1.2
buttonshim                       0.0.2
Cap1xxx                          0.1.3
certifi                          2018.8.24
chardet                          3.0.4
Click                            7.0
colorama                         0.3.7
colorzero                        1.1
cookies                          2.2.1
cryptography                     2.6.1
cupshelpers                      1.0
docutils                         0.14
drumhat                          0.1.0
entrypoints                      0.3
envirophat                       1.0.0
ExplorerHAT                      0.4.2
Flask                            1.0.2
fourletterphat                   0.1.0
gpiozero                         1.5.1
html5lib                         1.0.1
idna                             2.6
isort                            4.3.4
itsdangerous                     0.24
jedi                             0.13.2
Jinja2                           2.10
keyring                          17.1.1
keyrings.alt                     3.1.1
lazy-object-proxy                1.3.1
logilab-common                   1.4.2
lxml                             4.3.2
MarkupSafe                       1.1.0
mccabe                           0.6.1
microdotphat                     0.2.1
mote                             0.0.4
motephat                         0.0.3
mypy                             0.670
mypy-extensions                  0.4.1
numpy                            1.16.2
oauthlib                         2.1.0
olefile                          0.46
pantilthat                       0.0.7
parso                            0.3.1
pexpect                          4.6.0
pgzero                           1.2
phatbeat                         0.1.1
pianohat                         0.1.0
picamera                         1.13
piglow                           1.2.5
pigpio                           1.44
Pillow                           5.4.1
pip                              18.1
psutil                           5.5.1
pycairo                          1.16.2
pycrypto                         2.6.1
pycups                           1.9.73
pyftdi                           0.52.9
pygame                           1.9.4.post1
Pygments                         2.3.1
PyGObject                        3.30.4
pyinotify                        0.9.6
PyJWT                            1.7.0
pylint                           2.2.2
pyOpenSSL                        19.0.0
pyserial                         3.4
pysmbc                           1.0.15.6
python-apt                       1.8.4.3
pytz                             2021.1
pyusb                            1.1.1
pyxdg                            0.25
rainbowhat                       0.1.0
reportlab                        3.5.13
requests                         2.21.0
requests-oauthlib                1.0.0
responses                        0.9.0
roman                            2.0.0
rpi-ws281x                       4.2.6
RPi.GPIO                         0.7.0
RTIMULib                         7.2.1
schedule-machine                 0.1.0
scrollphat                       0.0.7
scrollphathd                     1.2.1
SecretStorage                    2.3.1
Send2Trash                       1.5.0
sense-hat                        2.2.0
setuptools                       40.8.0
simplejson                       3.16.0
six                              1.12.0
skywriter                        0.0.7
sn3218                           1.2.7
soupsieve                        1.8
spidev                           3.4
ssh-import-id                    5.7
sysv-ipc                         1.1.0
thonny                           3.3.5
touchphat                        0.0.1
twython                          3.7.0
typed-ast                        1.3.1
unicornhathd                     0.0.4
urllib3                          1.24.1
webencodings                     0.5.1
Werkzeug                         0.14.1
wheel                            0.32.3
wrapt                            1.10.11
```

