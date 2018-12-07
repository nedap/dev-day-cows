#!/usr/bin/env python

import random


# Return tag id ex '999-0000-00241234'
def get_sensor_id():
    return '999-0000-00238068'


# b.beacon
# b.rssi
# beacon.id
# beacon.x
# beacon.y
# beacon.z
# Return x,y,z
def calculatePosition(b1, b2, b3, b4):
    # What is b1, b2, b3, b4?
    rssiOfB1 = b1.rssi
    beaconInfoOfB2 = b2.beacon
    xOfB2 = beaconInfoOfB2.x
    # or
    xOfB2 = b2.beacon.x

    # Difficult math...
    # max screen size 2000cm
    x = random.random() * 2000
    y = 750
    # z is not used anyway, but a nice to have
    z = 0

    return x, y, z
