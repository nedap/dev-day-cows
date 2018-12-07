#!/usr/bin/env python

import socket
import json
import collections
from solution import getSensorId, calculatePosition

SENSOR_IP = 'p.q.r.s'
SENSOR_PORT = 9000
BUFFER_SIZE = 1024

START = "<start>"
END = "<end>"

MAP_IP = SENSOR_IP
MAP_PORT = 8000

Beacon = collections.namedtuple('Beacon', ['id', 'x', 'y', 'z'])
BEACON1 = Beacon(id=13, x=2500, y=2000, z=0)
BEACON2 = Beacon(id=11, x=1500, y=2000, z=0)
BEACON3 = Beacon(id=7, x=1400, y=800, z=0)
BEACON4 = Beacon(id=9, x=2400, y=1200, z=0)

BeaconWithRssi = collections.namedtuple('BeaconWithRssi', ['beacon', 'rssi'])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SENSOR_IP, SENSOR_PORT))

m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
m.connect((MAP_IP, MAP_PORT))

buffer = ""
while True:
    # print "Wait for sensor data...."
    data = s.recv(BUFFER_SIZE)
    # print "Sensor data received"
    buffer += data
    index = buffer.index(START)
    if (index == 0):
        index += len(START)
        buffer = buffer[index:]
    else:
        continue

    lines = buffer.split("\n")
    for line in lines:
        buffer = ""
        if (line.endswith(END)):
            line = line.replace(START, "")
            line = line.replace(END, "")
            sensor = json.loads(line)
            sensorId = sensor["sensorId"]
            beacons = sensor["beacons"]
            # print line
            if sensorId == getSensorId():
                beaconList = []
                for beacon in beacons:
                    beaconList.insert(int(beacon["beaconId"]), beacon["rssi"])
                print sensorId + ": ", beaconList
                # print line

                b1 = BeaconWithRssi(beacon=BEACON1, rssi=beaconList[BEACON1.id])
                b2 = BeaconWithRssi(beacon=BEACON2, rssi=beaconList[BEACON2.id])
                b3 = BeaconWithRssi(beacon=BEACON3, rssi=beaconList[BEACON3.id])
                b4 = BeaconWithRssi(beacon=BEACON4, rssi=beaconList[BEACON4.id])
                x, y, z = calculatePosition(b1, b2, b3, b4)

                x = int(x)
                y = int(y)

                print "Sent position to map: " + `x` + "," + `y`
                m.send(sensorId + "," + `x` + "," + `y` + "\n")
                print "Position sent to map"
                print "Wait for okay from map"
                data = m.recv(BUFFER_SIZE)
                print "Received result from map: ", data
        else:
            buffer = line;
s.close()
m.close();
