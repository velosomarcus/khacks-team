from openlch.hal import HAL

robot = HAL("192.168.42.1")

robot.servo.enable_movement()
robot.servo.set_positions([[i, 0] for i in range(1, 16)])