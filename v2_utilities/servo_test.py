from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device
Device.pin_factory = PiGPIOFactory()
from time import sleep

for i in range(1,28):
    print(f'servo pin: {i}')
    try:
        servo = Servo(i)
    except:
        print(f'error')
    else:
        print('min')
        servo.min()
        sleep(1)
        print('mid')
        servo.mid()
        sleep(1)
        print('max')
        servo.max()
        sleep(1)