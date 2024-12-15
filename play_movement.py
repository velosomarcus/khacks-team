import os
import sys
import json
import time

from openlch.hal import HAL


robot = HAL("192.168.42.1")

# filename = input("Enter the movement filename: ")
#
# full_file_path = os.path.join(os.getcwd(), (filename or "movements_up_down.json"))

if len(sys.argv) < 2:
    print("Usage: python script.py <file-name>")
    sys.exit(1)

# Get the parameter (first argument after the script name)
parameter = sys.argv[1]

full_file_path = os.path.join(os.getcwd(), parameter)
print(full_file_path)

if not os.path.isfile(full_file_path):
    print("File", full_file_path, "not found")
    sys.exit(0)


robot.servo.set_torque_enable([i, False] for i in range(1, 17))
robot.servo.set_torque([i, 50] for i in range(1,17))

input("hit Enter to start moving")
with open(full_file_path, 'r') as r:
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