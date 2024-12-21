import os
import sys
import json
import time

from openlch.hal import HAL


robot = HAL("192.168.42.1")

input('Hit Enter to relax the robot')
robot.servo.set_torque_enable([(i, False) for i in range(1, 17)])