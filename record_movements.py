import json
import time
from collections import defaultdict
from os import POSIX_SPAWN_OPEN

from openlch.hal import HAL

# Default IP is 192.168.42.1, which is the IP of the USB interface
robot = HAL("192.168.42.1")


# positions = robot.servo.get_positions()
suffix = input("Enter a filename for this movement:")
filename = 'movements_' + suffix + '.json'

robot.servo.disable_movement()

robot.servo.set_position(16, 0)

movements = []
# positions = robot
# .servo.get_positions()
robot.servo.set_torque_enable([(i, False) for i in range(1, 17)])
input("hit Enter when ready to start recording the movements")

start_time = time.time()
while time.time() - start_time < 12:
#while True:
    # Get current positions of all servos
    positions = robot.servo.get_positions()
    # ID, position, velocity [(1, 0, 0), (2, -50, 0), (3, 5, 20)...]
    # for item in positions:
    #     movements[item[0]].append(item)

    movements.append(positions)
    time.sleep(0.05)


with open(filename, 'w') as o:
    o.write(json.dumps(movements, indent=2))

print('Result:/n','Filename:', filename, 'Records:', len(movements))

# input("hit Enter to start moving")
# with open(filename, 'r') as r:
#     movements = json.loads(r.read())
#
# for key in movements:
#     for servo in key:
#         robot.servo.set_position(servo[0], servo[1]) #, .05)
#     time.sleep(0.01)
#
# robot.servo.set_torque_enable([(i, False) for i in range(1, 17)])