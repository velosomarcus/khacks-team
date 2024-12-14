import time
from openlch.hal import HAL

# Default IP is 192.168.42.1, which is the IP of the USB interface
robot = HAL("192.168.42.1")


# positions = robot.servo.get_positions()
input("hit Enter when ready to start moving")
robot.servo.set_position(16, 0)

movement_s16 = []
positions = robot.servo.get_positions()
input("hit Enter when ready to start recording the movements")

start_time = time.time()
while time.time() - start_time < 2:
    # Get current positions of all servos
    positions = robot.servo.get_positions()
    # ID, position, velocity [(1, 0, 0), (2, -50, 0), (3, 5, 20)...]
    for item in positions:
        if item[0] == 16:
            movement_s16.append(item)

    time.sleep(0.1)

print(movement_s16)

print(len(movement_s16), "positions saved")
    # print(type(positions))

input("hit Enter to start moving")

for item in movement_s16:
    robot.servo.set_position(item[0], item[1])
    time.sleep(0.1)

