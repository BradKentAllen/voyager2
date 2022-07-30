#!/usr/bin/env python
'''
file name: check_internet.py
date created: July 23, 2022
created by: Brad Allen
project/support: voyager2	# root or script it supports
description:

special instruction:
'''

import urllib.request


def check_URL(URL, URLtimout=10):
    '''checks input URL and returns True if connects
    '''
    try:
        with urllib.request.urlopen(URL, timeout = URLtimout) as page:
            print('connected with: ', URL)
            return True
    except urllib.error.URLError:
        print('ERROR connecting with: ', URL)
        return False
    except Exception:
        print('Error (type other) connecting')
        return False