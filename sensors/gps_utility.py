#!/usr/bin/env python
'''
file name:  gps_utility.py
date created:  August 24, 2022
created by: Brad Allen
project/support: voyager2 / NomiNomi      # root or script it supports
description:  Full package to get position from Ultimate GPS

Runs as an indendent self-test as well

rev 0.0.1 initial DEV
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'

import time
import serial

import adafruit_gps

class Ultimate_GPS:
    def __init__(self):
        '''Adafruit_Ultimate GPS
        The full GPS code has a host of options.
        Only the relevant code is used here

        Lat/Long are in degrees then minutes and decimal minutes (not decimal degrees)
        Latitude: DDMM.MMMM (The first two characters are the degrees.) 
        Longitude: DDDMM.MMMM (The first three characters are the degrees.
        '''

        uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

        self.gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

        # Turn on the basic GGA and RMC info (what you typically want)
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        
 
        #### Set GPS update rate (1 second)
        # Set update rate to once a second (1hz) which is what you typically want.
        self.gps.send_command(b"PMTK220,1000")


    def update(self):
        '''calls update function
        Must be called at least twice as fast as GPS update rate above
        '''
        self.gps.update()

    def read(self):
        '''returns GPS navigation readings
        '''
        if not self.gps.has_fix:
            return 'no fix', [0, 0, 0, 0 , 0, 0]
        else:
            gps_read = (self.gps.latitude, self.gps.longitude, self.gps.speed_knots, self.gps.track_angle_deg,\
                self.gps.satellites, self.gps.fix_quality)
            return 'good', gps_read 

    def read_time(self):
        '''Return time for use in setting clock
        XXXX needs work
        '''
        if not self.gps.has_fix:
            print('no fix')
        else:
            print(
                "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                    self.gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                    self.gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    self.gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    self.gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    self.gps.timestamp_utc.tm_min,  # month!
                    self.gps.timestamp_utc.tm_sec,
                )
            )

    def calc_distance(self, lat2, lon2, lat1, lon1):
        '''Return distance between two coordinates
        Distance is calculated in feet
        '''
        delta_lat = self.get_radians(lat2 - lat1)
        delta_lon = self.get_radians(lon2 - lon1)

        a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.sin(delta_lon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        earth_radius_miles = 3956

        # calculate distance in miles
        distance_miles = earth_radius_miles * c

        # convert to feet
        distance_feet = distance_miles * 5280

        return distance_feet


    def calc_bearing(lat2, lon2, lat1, lon1):
        '''calculate bearing from place 1 to place 2
        359,840 is 69.2 miles in feet
        '''
        bearing_radians = 0
    
        # calculate X and Y using longitude corrected by latitude
        Ydist = 359840 * (lat2 - lat1);
        Xdist = math.cos(3.14159 * ((lat2 + lat1) / 2) / 180) * 359840 * (lon2 - lon1);
  
        # calculate total distance
        dist = math.sqrt((Ydist * Ydist) + (Xdist * Xdist));
  
        # calculate bearing
        if Xdist >= 0 and Ydist > 0:
            bearing_radians = math.atan(Xdist / Ydist)
        elif Xdist > 0 and Ydist <= 0:
            bearing_radians = (math.pi * .5) + math.atan(-Ydist / Xdist)
        elif Xdist <= 0 and Ydist < 0:
            bearing_radians = math.pi + math.atan(Xdist / Ydist)
        elif Xdist < 0 and Ydist >= 0:
            bearing_radians = (math.pi * 1.5) + math.atan(-Ydist / Xdist)

        # convert to int degrees
        bearing = int(bearing_radians * 180 / math.pi)

        return bearing


if __name__ == "__main__":
    print('\ntesting Ultimate GPS in gps_utility.py')
    gps = Ultimate_GPS()
    flag = 0

    while True:
        gps.update()

        flag += 1
        if flag >= 4:
            flag = 0
            gps_reading = gps.read()
            print(f'{gps_reading[0]}: {gps_reading[1]}')
            print(gps.read_time())

        time.sleep(.3)






