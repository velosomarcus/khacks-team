import time
from openlch.hal import HAL

SERVO_NAME_TO_ID = {
    "left_shoulder_yaw": 15,
    "left_shoulder_pitch": 14,
    "left_elbow_yaw": 16,
    # "left_gripper": 14,
    "right_shoulder_yaw": 12,
    "right_shoulder_pitch": 13,
    "right_elbow_yaw": 11,
    # "right_gripper": 24,
    "left_hip_yaw": 9,
    "left_hip_roll": 8,
    "left_hip_pitch": 10,
    "left_knee_pitch": 7,
    "left_ankle_pitch": 6,
    "right_hip_yaw": 4,
    "right_hip_roll": 3,
    "right_hip_pitch": 5,
    "right_knee_pitch": 2,
    "right_ankle_pitch": 1,
}

robot = HAL("192.168.42.1")
print('Robot connected')

input('Hit Enter to relax the robot')
# relax the robot
robot.servo.set_torque_enable([(i, False) for i in range(1, len(SERVO_NAME_TO_ID) + 1)])
time.sleep(1)
robot.servo.enable_movement()
time.sleep(1)


# del robot
# robot = HAL("192.168.42.1")

input('Place the robot face down on the floor and hit Enter.')

input('Hit Enter to get the robot up from the ground')
robot.servo.disable_movement()
# robot.servo.enable_movement()
robot.servo.set_positions([[i, 0] for i in range(1, len(SERVO_NAME_TO_ID) + 1)])
time.sleep(1)

robot.servo.set_position(SERVO_NAME_TO_ID['right_hip_yaw'], -40)
robot.servo.set_position(SERVO_NAME_TO_ID['left_hip_yaw'], 40)

# robot.servo.set_position(SERVO_NAME_TO_ID['right_knee_pitch'], 15)
# robot.servo.set_position(SERVO_NAME_TO_ID['left_knee_pitch'], -15)

# robot.servo.set_position(SERVO_NAME_TO_ID['right_hip_roll'], -10)
# robot.servo.set_position(SERVO_NAME_TO_ID['left_hip_roll'], 10)

# robot.servo.set_position(SERVO_NAME_TO_ID['right_ankle_pitch'], 15)
# robot.servo.set_position(SERVO_NAME_TO_ID['left_ankle_pitch'], -15)

# robot.servo.set_position(SERVO_NAME_TO_ID['right_hip_pitch'], -15)
# robot.servo.set_position(SERVO_NAME_TO_ID['left_hip_pitch'], 15)

# robot.servo.set_position(SERVO_NAME_TO_ID['left_shoulder_yaw'], 25) #45
# robot.servo.set_position(SERVO_NAME_TO_ID['right_shoulder_yaw'], -25) #-45

# robot.servo.set_position(SERVO_NAME_TO_ID['right_elbow_yaw'], -45)
# robot.servo.set_position(SERVO_NAME_TO_ID['left_elbow_yaw'], 45)


SLEEP_INTERVAL = 0.8
MIN_ANGLE = 2
SMALL_ANGLE = 5
MIDDLE_ANGLE = 10
LARGE_ANGLE = 15

# start moving
for i in range(0, 60):
    print('loop:', i)
    current_positions = robot.servo.get_positions()
    # hip pitch up
    if i in range(0, 20):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_hip_pitch'],
             max(int(current_positions[SERVO_NAME_TO_ID['right_hip_pitch'] - 1][1] - SMALL_ANGLE), -90))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_hip_pitch'],
             min(int(current_positions[SERVO_NAME_TO_ID['left_hip_pitch'] - 1][1] + SMALL_ANGLE), 90))

    # hip pitch down
    if i in range(24, 31):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_hip_pitch'],
             min(int(current_positions[SERVO_NAME_TO_ID['right_hip_pitch'] - 1][1] + SMALL_ANGLE), 90))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_hip_pitch'],
             max(int(current_positions[SERVO_NAME_TO_ID['left_hip_pitch'] - 1][1] - SMALL_ANGLE), -90))

    # hip pitch down slowly
    if i in range(31, 48):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_hip_pitch'],
             min(int(current_positions[SERVO_NAME_TO_ID['right_hip_pitch'] - 1][1] + MIN_ANGLE), 90))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_hip_pitch'],
             max(int(current_positions[SERVO_NAME_TO_ID['left_hip_pitch'] - 1][1] - MIN_ANGLE), -90))

    # knee pitch up
    if i in range(0, 20):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_knee_pitch'],
             max(int(current_positions[SERVO_NAME_TO_ID['right_knee_pitch'] - 1][1] - SMALL_ANGLE), -90))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_knee_pitch'],
             min(int(current_positions[SERVO_NAME_TO_ID['left_knee_pitch'] - 1][1] + SMALL_ANGLE), 90))

    # knee pitch down
    if i in range(31, 46):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_knee_pitch'],
             min(int(current_positions[SERVO_NAME_TO_ID['right_knee_pitch'] - 1][1] + MIN_ANGLE), 90))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_knee_pitch'],
             max(int(current_positions[SERVO_NAME_TO_ID['left_knee_pitch'] - 1][1] - MIN_ANGLE), -90))

    # shoulder pitch up
    if i in range(4, 10):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_shoulder_pitch'],
             int(current_positions[SERVO_NAME_TO_ID['right_shoulder_pitch'] - 1][1] - LARGE_ANGLE))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_shoulder_pitch'],
             int(current_positions[SERVO_NAME_TO_ID['left_shoulder_pitch'] - 1][1] + LARGE_ANGLE))

    # elbow yaw up
    if i in range(4, 10):
        robot.servo.set_position(SERVO_NAME_TO_ID['left_elbow_yaw'],
             int(current_positions[SERVO_NAME_TO_ID['left_elbow_yaw'] - 1][1] - SMALL_ANGLE))
        robot.servo.set_position(SERVO_NAME_TO_ID['right_elbow_yaw'],
             int(current_positions[SERVO_NAME_TO_ID['right_elbow_yaw'] - 1][1] + SMALL_ANGLE))

    # elbow yaw down
    if i in range(10, 13):
        robot.servo.set_position(SERVO_NAME_TO_ID['left_elbow_yaw'],
             int(current_positions[SERVO_NAME_TO_ID['left_elbow_yaw'] - 1][1] + MIDDLE_ANGLE))
        robot.servo.set_position(SERVO_NAME_TO_ID['right_elbow_yaw'],
             int(current_positions[SERVO_NAME_TO_ID['right_elbow_yaw'] - 1][1] - MIDDLE_ANGLE))

    # shoulder yaw up
    if i in range(4, 8):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_shoulder_yaw'],
             int(current_positions[SERVO_NAME_TO_ID['right_shoulder_yaw'] - 1][1] - SMALL_ANGLE))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_shoulder_yaw'],
             int(current_positions[SERVO_NAME_TO_ID['left_shoulder_yaw'] - 1][1] + SMALL_ANGLE))

    # shoulder yaw down
    if i in range(8, 21):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_shoulder_yaw'],
             int(current_positions[SERVO_NAME_TO_ID['right_shoulder_yaw'] - 1][1] + SMALL_ANGLE))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_shoulder_yaw'],
             int(current_positions[SERVO_NAME_TO_ID['left_shoulder_yaw'] - 1][1] - SMALL_ANGLE))

    # ankle pitch up
    if (i in range(3, 4)
            or i in range(24, 29)
            or i in range(36, 40)):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_ankle_pitch'],
             int(current_positions[SERVO_NAME_TO_ID['right_ankle_pitch'] - 1][1] + MIN_ANGLE))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_ankle_pitch'],
             int(current_positions[SERVO_NAME_TO_ID['left_ankle_pitch'] - 1][1] - MIN_ANGLE))

    # ankle pitch down
    if i in range(13, 23):
        robot.servo.set_position(SERVO_NAME_TO_ID['right_ankle_pitch'],
             int(current_positions[SERVO_NAME_TO_ID['right_ankle_pitch'] - 1][1] - (SMALL_ANGLE * 2)))
        robot.servo.set_position(SERVO_NAME_TO_ID['left_ankle_pitch'],
             int(current_positions[SERVO_NAME_TO_ID['left_ankle_pitch'] - 1][1] + (SMALL_ANGLE * 2)))

    time.sleep(SLEEP_INTERVAL)




input('Hit Enter to relax the robot')
robot.servo.set_torque_enable([(i, False) for i in range(1, len(SERVO_NAME_TO_ID) + 1)])
