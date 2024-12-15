from openlch.hal import HAL

robot = HAL("192.168.42.1")

robot.servo.disable_movement()

# robot.servo.enable_movement()
robot.servo.set_positions([[i, 0] for i in range(1, 16)])

last_positions = {}
positions = robot.servo.get_positions()
for item in positions:
    last_positions[str(item[0])] = int(item[1])  # round(item[1], 1)


print(last_positions)

while True:
    current_positions = robot.servo.get_positions()
    no_changes = True
    for item in current_positions:
        if last_positions[str(item[0])] != int(item[1]):  # round(item[1], 1):
            last_positions[str(item[0])] = int(item[1])  # round(item[1], 1)
            print('servo:', item[0], 'value:', item[1])
            no_changes = False

    if not no_changes:
        print(last_positions)

#RightArm
#13:0
##12:-50
##11:-90
#13:-90