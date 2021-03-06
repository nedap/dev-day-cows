#!/usr/bin/env python

import socket
import json
import collections
from solution import get_sensor_id, calculate_position, get_team_name

SENSOR_IP = '192.168.88.254'  # Config this later
SENSOR_PORT = 9000
BUFFER_SIZE = 1024

START = "<start>"
END = "<end>"

MAP_IP = SENSOR_IP
MAP_PORT = 8000

Beacon = collections.namedtuple('Beacon', ['id', 'x', 'y', 'z'])
BEACON1 = Beacon(id=13, x=2500, y=2000, z=0)
BEACON2 = Beacon(id=11, x=1450, y=2000, z=0)
BEACON3 = Beacon(id=7, x=1500, y=800, z=0)
BEACON4 = Beacon(id=9, x=2400, y=1200, z=0)

BeaconRSSI = collections.namedtuple('BeaconWithRssi', ['beacon', 'rssi'])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SENSOR_IP, SENSOR_PORT))

mapper = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mapper.connect((MAP_IP, MAP_PORT))

buf = ""
while True:
    # Wait for sensor data...
    data = server.recv(BUFFER_SIZE)

    # Sensor data received!
    buf += data

    index = buf.index(START)
    if index == 0:
        index += len(START)
        buf = buf[index:]
    else:
        continue

    lines = buf.split("\n")

    for line in lines:
        buf = ""

        if line.endswith(END):
            line = line.replace(START, "")
            line = line.replace(END, "")
            sensor = json.loads(line)
            sensor_id = sensor["sensorId"]
            beacons = sensor["beacons"]

            if sensor_id == get_sensor_id():
                beacon_list = []
                for beacon in beacons:
                    beacon_list.insert(int(beacon["beaconId"]), beacon["rssi"])
                print sensor_id + ": ", beacon_list
                # print line

                b1 = BeaconRSSI(beacon=BEACON1, rssi=beacon_list[BEACON1.id])
                b2 = BeaconRSSI(beacon=BEACON2, rssi=beacon_list[BEACON2.id])
                b3 = BeaconRSSI(beacon=BEACON3, rssi=beacon_list[BEACON3.id])
                b4 = BeaconRSSI(beacon=BEACON4, rssi=beacon_list[BEACON4.id])

                x, y, z = calculate_position(b1, b2, b3, b4)

                x = int(x)
                y = int(y)

                position = str(x) + "," + str(y)
                print "Sending position to mapper: " + position
                mapper.send(get_team_name() + "," + position + "\n")
                print "Position sent to mapper"

                print "Wait for okay from mapper"
                data = mapper.recv(BUFFER_SIZE)
                print "Received result from map: ", data
        else:
            buf = line

server.close()
mapper.close()
