from openlch.hal import HAL
 
# Default IP is 192.168.42.1, which is the IP of the USB interface
robot = HAL("192.168.42.1")
 
# # Get current positions of all servos
positions = robot.get_positions()
# print(positions)
## ID, position, velocity [(1, 0, 0), (2, -50, 0), (3, 5, 20)...]
 
# Set position of individual servos
robot.servo.set_position(16, 0)  # Move servo ID 1 to 90 degrees
# robot.servo.set_position(2, -45, 20)  # Move servo ID 2 to -45 degrees at speed 20 deg/s
 
# # Set position of multiple servos
# robot.servo.enable_movement()  # Enable continuous position control
# robot.servo.set_positions([(1, 90), (2, -45), (3, 5)])  # Move servos to specified positions
 
# # Get IMU data
# imu_data = robot.imu.get_data()
# print(imu_data)
# ## {gyro: [x, y, z], accel: [x, y, z]}; units are deg/s and m/s^2 respectively