# Voyager Software



### Machine Type

MACHINE is defined in my_RPi_config.py.  

config.MACHINE determines the machine package imported in the imports of mechanic.py. 

config.custom_machine imports a machine in the home directory 

### Check for config variable

```
try:
	config.this_var
except NameError:
	print('nope')
else:
	print('yes')
```



## Modify Display Options

##### Step 1:  Modify scroll_dict in my_RPi_config

##### Step 2:  In machine init, add to scroll_machine if it requires a function/line

##### Step 3:  add function called at end of init



# GPIO

RPi_voyager is a wrapper around gpiozero.  GPIO objects are created using gpiozero then are stored in the gpio_func dictionary.  The actual gpiozero object is in gpio_func\['name of i/o']\[0] location.   The gpio_func dictionary then carries the key information for that input or output.

RPi_voyager can use either the standard RPI_GPIO (default) pin factory or pigpio (in config:  USE_PIGPIO = True).  The primary advantage of using pigpio is for servo control where the positioning is more precise and it prevents servos searching, which is common in the default RPI_GPIO.  The interface/API is the same for both but pigpio does require a daemon to be running to work.

```
#### to enable pigpio daemon:
sudo systemctl enable pigpiod
```

GPIO poses some issues with threading.  Both gpio libraries uses threads for various functions.  For example, button calls are on threads and their response, such as a function called, will be in a separate thread.  As such, you will need to be aware for unexpected results from gpio calls if you are not careful.

### gpio_func schema

'name' : (gpio object, pin, func_type, variable)

'name': string name for function

gpio object : created in create_gpio_function (in mechanic.py), this is the actual gpiozero object for that function

pin : integer for pin number (always BCM)

func_type : this is the type of function such as 'LED'.  Supported functions are:

* 'LED'
* 'button'
* 'input'
* 'servo'

note:  I2C sensors are supported differently so are not included here.

### Two ways to call gpio functions

Although it is possible to make gpio calls directly in the gpiozero 

##### Method 1:  driver.execute_gpio()

The driver.execute_gpio method runs through all gpio inputs or outputs in the gpio_func dictionary and makes sure they are set to the status in gpio_func[3].  This can be run very often, such as every poll or every second, but will cause problems if you have other time consuming functions at those times.

##### Method 2: driver.direct_drive_gpio(device, function, state)

The second method drives that output directly.  It both invokes the gpiozero object method and changes gpio_func[3] status to match the new state.  By carefully calling direct_drive_gpio you can avoid calling execute_gpio as often.

```
self.driver.direct_drive_gpio('red LED', 'off', None)

self.driver.direct_drive_gpio('blue LED 1', 'blink', (.5, .5))
```







