import os
import sys
import json
import time

from openlch.hal import HAL


robot = HAL("192.168.42.1")

filename = input("Enter the movement filename:")

filename = os.path.join(os.path.dirname(__file__), (filename or "movements_up_down.json"))


# if os.path.isfile(filename):
#     print("File", filename, "not found")
#     sys.exit(0)

robot.servo.set_torque_enable([i, False] for i in range(1, 17))
robot.servo.set_torque([i, 50] for i in range(1,17))

input("hit Enter to start moving")
with open(filename, 'r') as r:
    movements = json.loads(r.read())

robot.servo.set_torque_enable([i, True] for i in range(1, 17))
robot.servo.enable_movement()

for key in movements:
    print([[servo[0], servo[1]] for servo in key])
    robot.servo.set_positions([[servo[0], servo[1]] for servo in key])

    time.sleep(0.01)

robot.servo.disable_movement()

input('Hit Enter to relax the robot')
robot.servo.set_torque_enable([(i, False) for i in range(1, 17)])