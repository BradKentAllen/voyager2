import time
import board
# import digitalio # For use with SPI
import adafruit_bmp280


class BMP280:
    def __init__(self, sea_level_pressue=1013.25, I2C_address=0x76):
        # Create sensor object, communicating over the board's default I2C bus
        i2c = board.I2C()   # uses board.SCL and board.SDA
        self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)

        # reference sea level pressure
        self.bmp280.sea_level_pressure = 1013.25

    def get_pressure(self, in_Hg=False):
        '''returns pressure in millibar (hPa) or 
        inches mercury
        '''
        if in_Hg is True:
            return self.bmp280.pressure * .02953
        else:
            return self.bmp280.pressure

    def get_temp(self, F=False):
        '''returns temp in C or F
        '''
        if F is True:
            return (self.bmp280.temperature * 1.8) + 32
        else:
            return self.bmp280.temperature

        




if __name__ == '__main__':
    app = BMP280()
    while True:
        print(f"\nTemperature: {app.get_temp():0.1f} C")
        print(f"Temperature: {app.get_temp(F=True):0.1f} F")
        print(f"Pressure: {app.get_pressure():0.1f} hPa")
        print(f"Pressure: {app.get_pressure(in_Hg=True):0.1f} inches Hg")
        print("Altitude = %0.2f meters" % app.bmp280.altitude)
        time.sleep(2)