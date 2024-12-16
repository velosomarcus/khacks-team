from openlch.hal import HAL
 
# Default IP is 192.168.42.1, which is the IP of the USB interface
# robot = HAL("192.168.42.1")
 
# # Get current positions of all servos
#positions = robot.get_positions()
# print(positions)
## ID, position, velocity [(1, 0, 0), (2, -50, 0), (3, 5, 20)...]
 
#For servo 12, -50 is horizontal, 40 touches the hip
#For servo 11, 0 is flat, goes -90 to 90

# Set position of individual servos
# robot.servo.set_position(11, 0)  # Move servo ID 1 to 90 degrees
# robot.servo.set_position(12, 0)  # Move servo ID 1 to 90 degrees
# robot.servo.set_position(2, -45, 20)  # Move servo ID 2 to -45 degrees at speed 20 deg/s
 
# # Set position of multiple servos
# robot.servo.enable_movement()  # Enable continuous position control
# robot.servo.set_positions([(1, 90), (2, -45), (3, 5)])  # Move servos to specified positions
 
# # Get IMU data
# imu_data = robot.imu.get_data()
# print(imu_data)
# ## {gyro: [x, y, z], accel: [x, y, z]}; units are deg/s and m/s^2 respectively



robot = HAL("192.168.42.1")

#First stand up

robot.servo.disable_movement()

# robot.servo.enable_movement()
robot.servo.set_positions([[i, 0] for i in range(1, 16)])

robot.servo.set_position(4, -40)
robot.servo.set_position(9, 40)

robot.servo.set_position(2, -90)
robot.servo.set_position(7, -15)

#Servo ID to 0 is straight, 90 is backwards, -90 is forward

robot.servo.set_position(3, -10)
robot.servo.set_position(8, 10)

robot.servo.set_position(1, 90)

#Servo ID 1 to 0 is flat, -90 is tips pointed forward, 90 is inwards.

robot.servo.set_position(6, 0)

robot.servo.set_position(5, -15)
robot.servo.set_position(10, 15)

robot.servo.set_position(15, 45)
robot.servo.set_position(12, -45)

robot.servo.set_position(11, -45)
robot.servo.set_position(16, 45)