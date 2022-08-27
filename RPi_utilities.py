#!/usr/bin/env python
'''
file name:  RPi_utilities.py
date created: July 10, 2022
created by:  Brad Allen
project/support:  voyager2  ALL  # root or script it supports
description:

special instruction:
'''
__revision__ = 'v0.0.1'
__status__ = 'DEV' # 'DEV', 'alpha', 'beta', 'production'

import os
import subprocess   # for getting IP address
import pkg_resources  # part of setuptools
from datetime import datetime
import pytz


def get_time_stamp(local_time_zone='UTC', time_format='HMS'):
    now_local = datetime.now(pytz.timezone(local_time_zone))
    if time_format == 'YMD:HM':
        return now_local.strftime('%Y-%m-%d' + '-' + '%H:%M')
    else:
        return now_local.strftime('%H:%M:%S')

def get_time(local_time_zone='UTC'):
    now_local = datetime.now(pytz.timezone(local_time_zone))
    HH = now_local.strftime('%H')
    MM = now_local.strftime('%M')
    SS = now_local.strftime('%S')
    return (HH, MM, SS)

def get_hwclock_time():
    _current_time = os.system("sudo hwclock -r")
    time_str = "XXX INW:  HH:MM:SS"
    return time_str

#### RPI UTILITIES ####
def setRTC(year, month, date, hour, minute):
    # create and send time change to RTC
    timeEnter = 'sudo hwclock --set --date="' + str(year) + '-' + str(month)\
    + '-' + str(date) + ' ' + str(hour) + ':' + str(minute) + ':00"'
    #os.system('sudo hwclock --set --date="2011-08-14 16:45:05"')
    print('config input reset clock')
    print(timeEnter)
    os.system(timeEnter)

    # set RPI clock to RTC time (that was just set)
    os.system('sudo hwclock -s')
    print('set to: ', timeEnter)


def get_voyager_rev():
    '''Get s/w rev saved during startup
    '''
    # grabs current rev from its own .py file
    try:
        with open('voyager_VERSION.txt', 'r') as file:
            sw_rev = file.read()
            
    except FileNotFoundError as e:
        sw_rev = 'none'

    return sw_rev

def get_cpu_temp():
    '''returns RPi cpu temp as float degrees C
    '''
    f = open("/sys/class/thermal/thermal_zone0/temp", "r")
    t = int(f.readline ()) / 1000

    return t



def shutdown_RPi():
    #print('RPiUtilities shutdownRPI')
    os.system("sudo shutdown -h now")


def reboot_RPi():
    #print('RPiUtilities reboot')
    os.system("sudo reboot")

def get_IP_address():
    try:
        IPaddress = subprocess.getoutput('hostname -I')
    except subprocess.CalledProcessError:
        IPaddress = 'no IP'

    return IPaddress


#### USB Drive ####

def ejectUSB(usbPath):
    os.system('sudo umount ' + usbPath)
    print('usb ejected')

def findUSB():
    '''searches rpi for usb mounted by application: usbmount
    '''
    driveFound = 0
    # search the 7 usb directories for the thumb drive
    for i in ('0', '1', '2', '3', '4', '5', '6', '7'):
        usbPath = '/media/usb' + i
        # get a list of files in that directory, empty if no usb
        fileList = os.listdir(path=usbPath)
        if fileList != []:
            print('found usb drive on usb', i)
            # umount if more than one directory has a drive mounted
            if driveFound == 1:
                print('eject drive on usb', i)
                utilities.ejectUSB(usbPath)
            else:
                driveFound = 1
                return usbPath
    print('dir used is ', usbPath)

#### File Management Methods ####
def get_directory_size(dir_path, use_cwd=True):
    '''walk a directory tree and total up size of all files
    dir_path is combined with current working directory
    Return is size in MB
    A non-existent directory returns 0 mb
    '''
    total_size = 0
    if use_cwd == True:
        cwd = os.getcwd()
        start_path = os.path.join(cwd, dir_path)  # To get size of current directory
    else:
        start_path = dir_path

    for path, dirs, files in os.walk(start_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)

    mb_size = int(total_size / 1000000)

    return mb_size

#### Software Update ####

def copy_SW(usb_path, usb_file_pathname, file_pathname, sudo=False):
    command = 'cp -r ' + usb_path + usb_file_pathname + '/. /home/pi/' + file_pathname + '/'

    if sudo == True:
        command = 'sudo ' + command

    os.system(command)
    print('copy new software: ')
    print(command)

#### WIFI ####
def get_wifi_network():
    return subprocess.getoutput('iwgetid')[17:-1]

def gen_wpa_supplicant(usb_path, wifi_file_pathname):
    '''check for wifi file
    WARNING: must be running as sudo!!!!
    Format for wifi file is:
    .txt file
    one line per network in priority order
    ssid, password,
    '''
    print('update wifi')
    print(usb_path)
    print(wifi_file_pathname)
    if usb_path is None:
        return 'no usb_path'

    if wifi_file_pathname is None:
        return 'no wifi file'

    try:
        with open(usb_path + '/' + wifi_file_pathname, 'r') as file:
            # read full file
            line_list = file.readlines()
            
    except FileNotFoundError as e:
        return 'no wifi file'

    else:
        #print(line_list)
        #print(type(line_list))
        for count, line in enumerate(line_list):
            if len(line) != 0:
                # remove line breaks
                line = line.replace('\n', '')
                # remove double commas (this can happen at end of line)
                line = line.replace(',,', '')
                # remove trailing comma if it exists
                #print('line:')
                #print(line)
                if line[-1:] == ',':
                    network = line[:-1]
                network = line.split(',')
                # remove empty strings
                network = [x for x in network if x]
                #print('network')
                #print(network)
                if len(network) == 2:
                    if count == 0:
                        utilities.create_wpa_supplicant()
                    # remove white spaces from ssid and password
                    ssid = network[0].strip()
                    password = network[1].strip()
                    utilities.add_network(ssid, password)
                else:
                    if count == 0:
                        return 'bad wifi file'
            else:
                    if count == 0:
                        return 'empty wifi file'
        return 'created wpa_supplicant'

def copy_wpa_supplicant():
    print('copy wpa_supplicant')
    os.system("sudo cp wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf")

def create_wpa_supplicant():
    '''creates basic wpa_supplicant heading
    '''
    with open('wpa_supplicant.conf', 'w') as file:
        file.write('country=US')
        file.write('\n')
        file.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev')
        file.write('\n')
        file.write('update_config=1')
        file.write('\n\n')


def add_network(ssid, password):
    '''adds network to wpa_supplicant.conf that already has header
    '''
    try:
        with open('wpa_supplicant.conf', 'r') as file:
            print('add network')

    except FileNotFoundError:
        print('error, no wpa_supplicant file')

    else:
        # add heading for existing file
        with open('wpa_supplicant.conf', 'a') as file:
            file.write('network={')
            file.write('\n')
            file.write(f'ssid="{ssid}"')
            file.write('\n')
            file.write('scan_ssid=1')
            file.write('\n')
            file.write(f'psk="{password}"')
            file.write('\n')
            file.write('key_mgmt=WPA-PSK')
            file.write('\n')
            file.write('}')
            file.write('\n')

            
        






