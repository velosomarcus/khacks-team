import os
import sys
import json
import time
from readchar import readchar

from openlch.hal import HAL


# Get the parameter (first argument after the script name)

robot = HAL("192.168.42.1")
const_speed = 0.3
######
def stand_up():
    robot.servo.disable_movement()

    robot.servo.set_positions([[i, 0] for i in range(1, 16)])

    robot.servo.set_position(4, -42)
    robot.servo.set_position(9, 42)

    robot.servo.set_position(2, 83)
    robot.servo.set_position(7, -83)

    robot.servo.set_position(1, 57)
    robot.servo.set_position(6, -45)

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

def guard_pose_right():
    # gard pose
    set_servo_position(12, 45)
    set_servo_position(11, -90)

    time.sleep(const_speed)
    
def guard_pose_left():
    set_servo_position(15, -45)
    set_servo_position(16, 90)

    time.sleep(const_speed)

def prepare_to_punch_right():
    set_servo_position(12, -45)
    set_servo_position(11, -90)
    set_servo_position(13, -90)

    time.sleep(const_speed)

def prepare_to_punch_left():
    set_servo_position(15, 45)
    set_servo_position(16, 90)
    set_servo_position(14, 90)

    time.sleep(const_speed)

def rightpunch():
    set_servo_position(12, 45)
    set_servo_position(11, -10)
    time.sleep(const_speed)
    set_servo_position(12, -45)
    set_servo_position(11, -90)

    time.sleep(const_speed)
    
def leftpunch():
    set_servo_position(15, -45)
    set_servo_position(16, 10)
    time.sleep(const_speed)
    set_servo_position(15, 45)
    set_servo_position(16, 90)

    time.sleep(const_speed)

def right_uppercut():
    set_servo_position(12, 40)
    set_servo_position(11, -10)
    set_servo_position(13, 0)
    time.sleep(const_speed)
    set_servo_position(12, 40)
    set_servo_position(11, -10)
    set_servo_position(13, -90)
    time.sleep(const_speed)
    
def left_uppercut():
    set_servo_position(15, -40)
    set_servo_position(16, 10)
    set_servo_position(14, 0)
    time.sleep(const_speed)
    set_servo_position(15, -40)
    set_servo_position(16, 10)
    set_servo_position(14, 90)

    time.sleep(const_speed)

# stand up
stand_up()
# trying to speed up robot start up
robot.servo.get_positions()

# right arm down

# # gard pose
# gard_pose()
# position to punch

# set_servo_position(12, -45)
# set_servo_position(11, -90)
# set_servo_position(13, -90)
#time.sleep(0.5)

# guard pose

print("Press 'a' for right punch, 'l' for left punch, 's' for right uppercut, 'k' for left uppercut, 'j' for guard right, 'd' for guard left, or 'q' to quit")
while True:
    try:
        key = readchar().lower() 
        if key == 'l':
            prepare_to_punch_right()
            rightpunch()
        elif key == 'a':
            prepare_to_punch_left()
            leftpunch()
        elif key == 'j':
            guard_pose_right()
        elif key == 'd':
            guard_pose_left()
        elif key == 'k':
            right_uppercut()
        elif key == 's':
            left_uppercut()
        elif key == 'q':
            break
    except KeyboardInterrupt:
        break

# stand pose
# set_servo_position(11, 0)
# set_servo_position(12, 0)
# time.sleep(0.3)
# set_servo_position(13, 0)

robot.servo.set_torque_enable([(i, False) for i in range(11, 17)])
