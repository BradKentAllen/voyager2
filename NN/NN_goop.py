#!/usr/bin/env python
'''
file name:  NN_goop.py
date created:  August 27, 2022
created by:  Brad Allen
project/support: NomiNomiV2           # root or script it supports
description:

special instruction:
'''
from dataclasses import dataclass

@dataclass
class Goop():
    ''' data
    '''
    ### Sailboat Sensor Data ####
    heading_compass: int = 999 # read from magnetometer
    heading_boat: int = 999 # compensated to result in boat heading
    heading_course: int = 999 # calculated in navigation
    # note: heading_differential is a local variable only

    wind_zone: str = None
    heel: int = 999

    gps_fix: bool = False
    gps_lon: float = 0.0
    gps_lat: float = 0.0

    #### Sailboat Sailing Data ####
    sailing: bool = False   # tells is in sailing mode
    sail_mode: str = 'close'  # irons, tacking, close, broad, run, jibing
    # boat settings (servos set to these parameters)
    # rudder_angle: positive is to starboard (servo input is 90 + rudderAngle)
    rudder_angle_port: int = 0
    rudder_angle_starboard: int = 0
    main_sail_sheet: int = 0  #
    jib_sail_sheet: int = 0  # angle for servo setting


    #### Sailboat Navigation Data ####
    target_lat: float = 0.0
    target_lon: float = 0.0
    
    home_lat: float = 0.0
    home_lon: float = 0.0

    # heading_course is above in sailboat sensor data

    #### NomiNomi Boat Parameters ####
    RUDDER_ANGLE_MAX: int = 35
    RUDDER_BIAS_WEIGHT: int = 8  # 4 results in rudder_angle = heading_delta

    ROLL_ANGLE_TARGET: int = 10 # sheet in under this
    ROLL_ANGLE_MAX: int = 45  # take urgent action to correct over this
    
    IRONS_ANGLE: int = 25
    TACK_TARGET_ANGLE: int = 50
    CLOSE_ANGLE: int = 75
    RUN_ANGLE: int = 155

    SAIL_SERVO_PULSE_MIN: int = 1000
    SAIL_SERVO_PULSE_MAX: int = 2400

    # Compass adjusters are subtracted from reading to get true bearing
    # e.g. declination of 11 means true North is at 349 degrees
    COMPASS_DECLINATION: int = 0  # nature of the area
    COMPASS_OFFSET: int = 0  # calibration value for magnemometer

    

    #### general voyager2 parameters ####
    main_thread_inhibit: bool = False  # inhibits main thread, particular for button thread
    startup_seconds: int = 15 # must be greater than 10 seconds
    flash_flag: bool = True

    button1: bool = False
    button2: bool = False
    button3: bool = False

    # ### buttons args
    ''' used for passing arguements to button functions in UI
    '''
    button1_args = {}
    button2_args = {}
    button3_args = {}

    # ### Screens
    current_screen_group: str = 'home'
    current_screen: str = 'main'

    ''' init_UI flag
    if True, then will init UI.  Typically this includes new button functions
    '''
    init_UI: bool = False 


    