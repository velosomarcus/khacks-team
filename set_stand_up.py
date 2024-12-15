from openlch.hal import HAL

robot = HAL("192.168.42.1")

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

robot.servo.set_position(15, 20)
robot.servo.set_position(12, -20)

robot.servo.set_position(11, -45)
robot.servo.set_position(16, 45)