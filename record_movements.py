import time
from openlch.hal import HAL

# Default IP is 192.168.42.1, which is the IP of the USB interface
robot = HAL("192.168.42.1")


# positions = robot.servo.get_positions()

start_time = time.time()
# while time.time() - start_time < 5:
#     # Get current positions of all servos
positions = robot.servo.get_positions()
    ## ID, position, velocity [(1, 0, 0), (2, -50, 0), (3, 5, 20)...]
print(positions)
print(type(positions))

print(type(positions[0]))
# time.sleep(0.1)  # Pause for 1 second between prints
positions0 = robot.servo.get_positions()
for item in positions0:
    if item[0] == 16:
        print(item[0])
        break
