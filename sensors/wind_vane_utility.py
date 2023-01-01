#!/usr/bin/env python
'''
file name:  wind_vane_utility.py
date created:  August 22, 2022
created by: Brad Allen
project/support: voyager2 / NomiNomi      # root or script it supports
description:  Full package to read wind using ADS1115 A to D converter

Runs as an indendent self-test as well

rev 0.0.1 initial DEV
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'

import bisect

try:
    import ads1115driver as ADC
except ModuleNotFoundError:
    import sensors.ads1115driver as ADC


class Wind_Vane:
    def __init__(self):
        '''Set up ADS1115
        '''
        print('\n\n### init Wind Vane)')
        #### Instantiate sensor object

        # I2C address can be adjusted or assigned here
        self.sense_ads1115 = ADC.ADS1115(
            address=0x48,
            )

        #### Sensor data
        self.volt_0 = 0.0
        self.volt_1 = 0.0
        self.volt_2 = 0.0
        self.volt_3 = 0.0



        ####################################
        #### Create tools for wind vane ####
        #### and associated wind zones #####
        ####################################
        # wind vane and zone is run here so the 
        # lists, dictionaries, and such are only created once
        wind_chart = {
            'S5': ((0, .24), (120,135)),
            'S3': ((.24, .285), (60,80)),
            'S4': ((0.285, .35), (80,120)),
            'S7': ((.35, .50), (150,170)),
            'S6': ((.50, .69), (135,150)),
            'P7': ((.69, .85), (150,170)),
            'Z8': ((.85, 1.11), (170, 180)),
            'S1': ((1.11, 1.40), (15,35)),
            'S2': ((1.40, 1.71), (35,60)),
            'P5': ((1.71, 1.98), (120,135)),
            'P6': ((1.98, 2.14), (135,150)),
            'P1': ((2.14, 2.39), (15, 35)),
            'A0': ((2.39, 2.6), (0,15)),
            'P3': ((2.6, 2.76), (60,80)),
            'P2': ((2.76, 2.95), (35,60)),
            'P4': ((2.95, 4.0), (80,120)),
            }

        # These three lists are used by the read_wind function
        # to find the wind zone
        _zones = list(wind_chart.keys())
        self.zones_list = [item for item in _zones]

        _values_list = list(wind_chart.values())
        self.wind_mins = [item[0][0] for item in _values_list]
        self.wind_maxs = [item[0][1] for item in _values_list]

        #### Wind Target Angles
        # These three lists are used to determine wind_target
        _angles_mins = [item[1][0] for item in _values_list]
        _angles_maxs = [item[1][1] for item in _values_list]

        self.wind_zone_angles = {
            'port_zones': [],
            'port_mins': [],
            'port_maxs': [],
            'starboard_zones': [],
            'starboard_mins': [],
            'starboard_maxs': [],
            }

        # fill wind_zone_angles but not ordered
        self.wind_zone_angles['port_zones'] = [x for x in self.zones_list if x in ('A0', 'Z8') or x[0] == 'P']
        self.wind_zone_angles['starboard_zones'] = [x for x in self.zones_list if x in ('A0', 'Z8') or x[0] == 'S']
        for count, item in enumerate(self.zones_list):
            if item in self.wind_zone_angles['port_zones']:
                self.wind_zone_angles['port_mins'].append(_angles_mins[count])
                self.wind_zone_angles['port_maxs'].append(_angles_maxs[count])
            if item in self.wind_zone_angles['starboard_zones']:
                self.wind_zone_angles['starboard_mins'].append(_angles_mins[count])
                self.wind_zone_angles['starboard_maxs'].append(_angles_maxs[count])

        # put wind_zone_angles lists into order
        _port_list = [[x, 0, 0] for x in self.wind_zone_angles.get('port_zones')]
        for count, item in enumerate(_port_list):
            _port_list[count][1] = self.wind_zone_angles.get('port_mins')[count]
            _port_list[count][2] = self.wind_zone_angles.get('port_maxs')[count]

        _starboard_list = [[x, 0, 0] for x in self.wind_zone_angles.get('starboard_zones')]
        for count, item in enumerate(_port_list):
            _starboard_list[count][1] = self.wind_zone_angles.get('starboard_mins')[count]
            _starboard_list[count][2] = self.wind_zone_angles.get('starboard_maxs')[count]

        # sort in order of the zone #'s
        _port_list.sort(key= lambda x:x[0][1])
        _starboard_list.sort(key= lambda x:x[0][1])

        # feed back into wind_zone_angles
        self.wind_zone_angles = {
            'port_zones': [],
            'port_mins': [],
            'port_maxs': [],
            'port_zone_angles': {},
            'starboard_zones': [],
            'starboard_mins': [],
            'starboard_maxs': [],
            'starboard_zone_angles': {},
            }

        for item in _port_list:
            self.wind_zone_angles['port_zones'].append(item[0])
            self.wind_zone_angles['port_mins'].append(item[1])
            self.wind_zone_angles['port_maxs'].append(item[2])
            self.wind_zone_angles['port_zone_angles'][item[0]] = int((item[2] + item[1]) / 2)
        for item in _starboard_list:
            self.wind_zone_angles['starboard_zones'].append(item[0])
            self.wind_zone_angles['starboard_mins'].append(item[1])
            self.wind_zone_angles['starboard_maxs'].append(item[2])
            self.wind_zone_angles['starboard_zone_angles'][item[0]] = int((item[2] + item[1]) / 2)

        '''
        print('\n\n### DEBUG ###')
        print(self.zones_list)
        print(self.wind_mins)
        print(self.wind_maxs)
        for key, value in self.wind_zone_angles.items():
            print(f'{key} - {value}')
        '''

    def get_zone(self, tack, angle):
        '''XXXX - not sure why this was here
        Note that zone_dict is not referenced anywhere
        '''
        if tack == 'port':
            idx = bisect.bisect_left(zone_dict.get('port_maxs'), angle)
            if idx < len(zone_dict['port_maxs']) and zone_dict['port_mins'][idx] <= angle <= zone_dict['port_maxs'][idx]:
                zone = zone_dict['port_zones'][idx]
            else:
                zone = None
        else:
            idx = bisect.bisect_left(zone_dict.get('starboard_maxs'), angle)
        if idx < len(zone_dict['starboard_maxs']) and zone_dict['starboard_mins'][idx] <= angle <= zone_dict['starboard_maxs'][idx]:
            zone = zone_dict['starboard_zones'][idx]
        else:
            zone = None
    
        return zone

    def read_wind(self):
        '''Read wind voltage
        Convert to zone
        Returns None for error
        '''
        wind_volts = self.get_volt0(True, False)  
        #print(f'wind_volts: {wind_volts}')

        # check if bad sensor or before first sense
        if wind_volts is None:
            print('wind volts read zero')
            return None

        idx = bisect.bisect_left(self.wind_maxs, wind_volts)
        if idx < len(self.wind_maxs) and self.wind_mins[idx] <= wind_volts <= self.wind_maxs[idx]:
            return self.zones_list[idx]
        else:
            print('wind zone read error')
            return None

    # #################################
    # #### ADS1115 Utility Methods ####
    # #################################

    def update_data(self):
        '''Read sensor using sensor driver
        DeviceRangeError returns ???
        '''
        # Read channel 0
        try:
            self.volt_0 = self.sense_ads1115.readADCSingleEnded(0)
        except OSError:
            print(f'ADS1115 A to D channel 0 did not read correctly')

        # Read channel 1
        try:
            self.volt_1 = self.sense_ads1115.readADCSingleEnded(1)
            # print(f'\n\n&&&&& read volt_1: {self.volt_1}')
        except OSError:
            print(f'ADS1115 A to D channel 1 did not read correctly')

        # Read channel 2
        try:
            self.volt_2 = self.sense_ads1115.readADCSingleEnded(2)
        except OSError:
            print(f'ADS1115 A to D channel 2 did not read correctly')

        # Read channel 3
        try:
            self.volt_3 = self.sense_ads1115.readADCSingleEnded(3)
            # print(f'\n\n&&&&& read volt_3: {self.volt_3}')
        except OSError:
            print(f'ADS1115 A to D channel 3 did not read correctly')

        

    def get_volt0(self, update=True, format=True):
        '''Primary method for getting volt
        Returns volts
        update=False saves processing if other data was collected first
        '''
        if update == True:
            self.update_data()

        # convert mv to volts
        volts = self.volt_0 / 1000

        if format == True:
            return f'{volts:.2f}'
        else:
            return volts

    def get_volt1(self, update=True, format=True):
        '''Primary method for getting volt
        Returns volts
        update=False saves processing if other data was collected first
        '''
        if update == True:
            self.update_data()

        # convert mv to volts
        volts = self.volt_1 / 1000

        if format == True:
            return f'{volts:.2f}'
        else:
            return volts

    def get_volt2(self, update=True, format=True):
        '''Primary method for getting volt
        Returns volts
        update=False saves processing if other data was collected first
        '''
        if update == True:
            self.update_data()

        # convert mv to volts
        volts = self.volt_2 / 1000

        if format == True:
            return f'{volts:.2f}'
        else:
            return volts

    def get_volt3(self, update=True, format=True):
        '''Primary method for getting volt
        Returns volts
        update=False saves processing if other data was collected first
        '''
        if update == True:
            self.update_data()

        # convert mv to volts
        volts = self.volt_3 / 1000

        if format == True:
            return f'{volts:.2f}'
        else:
            return volts


# #############################
# #### self-contained test ####
# #############################

if __name__ == "__main__":
    import time

    wind_vane = Wind_Vane()

    while True:
        wind = wind_vane.read_wind()
        print(f'wind: {wind}')
        time.sleep(1)




