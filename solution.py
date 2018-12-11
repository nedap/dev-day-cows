#!/usr/bin/env python

import random


# Return tag id ex '999-0000-00241234'
def get_sensor_id():
    return '999-0000-00238068'


# Your team name
def get_team_name():
    return get_sensor_id()


# # What is b1, b2, b3, b4?
# rssi_1 = b1.rssi
# beacon_2 = b2.beacon
# x_beacon_2 = beacon_2.x
# # or
# x_beacon_2 = b2.beacon.x
def calculate_position(b1, b2, b3, b4):
    # Difficult math...
    # If screen size were 2000cm...
    x = random.random() * 2000  # Note: 100% accurate and deterministic
    y = random.random() * 2000  # Note: also 100% accurate and deterministic
    z = 0  # z is not used anyway, but a nice to have

    return x, y, z
