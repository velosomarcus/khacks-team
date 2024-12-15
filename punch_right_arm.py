import os
import sys
import json
import time

from openlch.hal import HAL


robot = HAL("192.168.42.1")

input("hit Enter to start moving")

######

robot.servo.disable_movement()

# robot.servo.enable_movement()
robot.servo.set_positions([[i, 0] for i in range(1, 16)])

robot.servo.set_position(4, -40)
robot.servo.set_position(9, 40)

robot.servo.set_position(2, 15)
robot.servo.set_position(7, -15)

robot.servo.set_position(3, -10)
robot.servo.set_position(8, 10)

robot.servo.set_position(1, 15)
robot.servo.set_position(6, -15)

robot.servo.set_position(5, -15)
robot.servo.set_position(10, 15)

robot.servo.set_position(15, 45)
robot.servo.set_position(12, -45)

robot.servo.set_position(11, -45)
robot.servo.set_position(16, 45)
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

def gard_pose(arm):
    # gard pose
    if arm == 'right':
        set_servo_position(12, 45)
        set_servo_position(11, -90)
    time.sleep(0.5)

def prepare_to_punch(arm):
    if arm == 'right':
        set_servo_position(12, -45)
        set_servo_position(11, -90)
        set_servo_position(13, -90)
        time.sleep(0.3)

def punch(arm):
    if arm == 'right':
        set_servo_position(12, 45)
        set_servo_position(11, 0)
        time.sleep(0.3)
        set_servo_position(12, -45)
        set_servo_position(11, -90)
        time.sleep(0.3)

# trying to speed up robot start up
robot.servo.get_positions()

# right arm down
set_servo_position(13, 0)
# # gard pose
# gard_pose()
# position to punch
prepare_to_punch('right')
# set_servo_position(12, -45)
# set_servo_position(11, -90)
# set_servo_position(13, -90)
time.sleep(0.5)

# punch
punch('right')
# set_servo_position(12, 45)
# set_servo_position(11, 0)
# time.sleep(0.3)
# back
# set_servo_position(12, -45)
# set_servo_position(11, -90)
# time.sleep(0.5)
# punch again
punch('right')
# set_servo_position(12, 45)
# set_servo_position(11, 0)
# time.sleep(0.3)
# gard pose
gard_pose('right')

# stand pose
set_servo_position(11, 0)
time.sleep(0.3)
set_servo_position(13, 0)






input('Hit Enter to relax the robot')
robot.servo.set_torque_enable([(i, False) for i in range(11, 17)])
