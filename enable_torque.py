from openlch.hal import HAL
import sys
# Default IP is 192.168.42.1, which is the IP of the USB interface

# 1 is right foot
# 2 is right knee
# 3 is right hip twisting
# 4 is right hip abd
# 5 is right hip pitch
# 6 is left ankle
# 7 is left knee
# 8 is left hip twisting
# 9 is left hip abd
# 10 is left hip pitch
# 11 is right wrist
# 12 is right shoulder pitch
# 13 is right shoulder twist
# 14 is left twist
# 15 is left shoulder pitch
# 16 is left elbow


servo_map = {
    'left_leg': [6, 7, 8, 9, 10],
    'right_leg': [1, 2, 3, 4, 5],
    'right_arm': [11, 12, 13],
    'left_arm': [14, 15, 16],
    'everything': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
}

def enable_torque(group='everything'):
    robot = HAL("192.168.42.1")
    robot.servo.enable_movement()


    robot.servo.set_torque_enable([(i, True) for i in servo_map[group]])

group='everything'
if len(sys.argv) > 1:
    group = sys.argv[1]

enable_torque(group)
