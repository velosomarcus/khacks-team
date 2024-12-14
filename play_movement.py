import os
import sys
import json
import time

from openlch.hal import HAL


robot = HAL("192.168.42.1")

filename = input("Enter the movement filename:")

if os.path.isfile(filename):
    print("File", filename, "not found")
    sys.exit(0)

input("hit Enter to start moving")
with open(filename, 'r') as r:
    movements = json.loads(r.read())

for key in movements:
    for servo in key:
        robot.servo.set_position(servo[0], servo[1]) #, .05)
    time.sleep(0.01)

robot.servo.set_torque_enable([(i, False) for i in range(1, 17)])