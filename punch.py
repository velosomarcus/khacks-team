import os
import sys
import json
import time

from openlch.hal import HAL


robot = HAL("192.168.42.1")

input("hit Enter to start moving")

######
def stand_up():
    robot.servo.disable_movement()

    robot.servo.set_positions([[i, 0] for i in range(1, 16)])

    robot.servo.set_position(4, -42)
    robot.servo.set_position(9, 42)

    robot.servo.set_position(2, 83)
    robot.servo.set_position(7, -83)

    robot.servo.set_position(1, 57)
    robot.servo.set_position(6, -57)

    robot.servo.set_position(5, -31)
    robot.servo.set_position(10, 31)

#####
# {'1': 57, '2': 82, '3': 0, '4': -42, '5': -31, '6': -57, '7': -83, '8': 0, '9': 42, '10': 31, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0}
#####

def set_servo_position(servo_id, position):
    robot.servo.set_position(servo_id, position)
    # check_servo_position(servo_id, position)

def check_servo_position(servo_id, position):
    while True:
        for item in robot.servo.get_positions():
            if item[0] == servo_id:
                if int(position)-1 <= int(item[1]) <= int(position) + 1:
                    return
                else:
                    print(item[1], position)

def guard_pose(arm):
    # gard pose
    if arm == 'right':
        set_servo_position(12, 45)
        set_servo_position(11, -90)
    elif arm == 'left':
        set_servo_position(15, -45)
        set_servo_position(16, 90)

    time.sleep(0.5)

def prepare_to_punch(arm):
    if arm == 'right':
        set_servo_position(12, -45)
        set_servo_position(11, -90)
        set_servo_position(13, -90)
    elif arm == 'left':
        set_servo_position(15, 45)
        set_servo_position(16, 90)
        set_servo_position(14, 90)

    time.sleep(0.3)

def punch(arm):
    if arm == 'right':
        set_servo_position(12, 45)
        set_servo_position(11, -10)
        time.sleep(0.5)
        set_servo_position(12, -45)
        set_servo_position(11, -90)
    elif arm == 'left':
        set_servo_position(15, -45)
        set_servo_position(16, 10)
        time.sleep(0.5)
        set_servo_position(15, 45)
        set_servo_position(14, 90)

    time.sleep(0.3)


# stand up
stand_up()
# trying to speed up robot start up
robot.servo.get_positions()

# right arm down
set_servo_position(13, 0)
# # gard pose
# gard_pose()
# position to punch
prepare_to_punch('right')
prepare_to_punch('left')
# set_servo_position(12, -45)
# set_servo_position(11, -90)
# set_servo_position(13, -90)
#time.sleep(0.5)

# punch
punch('right')
# punch
punch('right')
# punch
punch('left')

# guard pose
guard_pose('right')
guard_pose('left')

# stand pose
# set_servo_position(11, 0)
# set_servo_position(12, 0)
# time.sleep(0.3)
# set_servo_position(13, 0)


input('Hit Enter to relax the robot')
robot.servo.set_torque_enable([(i, False) for i in range(11, 17)])
