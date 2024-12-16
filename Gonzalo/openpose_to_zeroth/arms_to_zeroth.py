import cv2
import mediapipe as mp
import time
import numpy as np
from openlch.hal import HAL

# Initialize robot connection
robot = HAL("192.168.42.1")

#First stand up

robot.servo.disable_movement()

# robot.servo.enable_movement()
robot.servo.set_positions([[i, 0] for i in range(1, 16)])

robot.servo.set_position(4, -40)
robot.servo.set_position(9, 40)

robot.servo.set_position(2, 15)
robot.servo.set_position(7, -15)

robot.servo.set_position(3, -10)
robot.servo.set_position(8, 10)

robot.servo.set_position(1, 10)
robot.servo.set_position(6, -8)

robot.servo.set_position(5, -15)
robot.servo.set_position(10, 15)

robot.servo.set_position(15, 45)
robot.servo.set_position(12, -45)

robot.servo.set_position(11, -45)
robot.servo.set_position(16, 45)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)
mp_drawing = mp.solutions.drawing_utils

# Servo ID mapping
SERVO_MAPPING = {
    'right_elbow': 11,
    'right_shoulder': 12,
    'left_shoulder': 15,
    'left_elbow': 16
}

# Angle adjustment parameters for each servo
SERVO_ADJUSTMENTS = {
    'right_shoulder': {'offset': 50, 'scale': -1.0},  # Invert and shift by 90 degrees
    'right_elbow': {'offset': -90, 'scale': 1.0},      # Scale by 0.8 and shift by 45 degrees
    'left_shoulder': {'offset': -40, 'scale': -1.0},   # Scale by 1.2 and shift by -30 degrees
    'left_elbow': {'offset': 90, 'scale': 1.0}         # No adjustment
}

# Add these constants after the SERVO_MAPPING
BODY_LANDMARKS = [
    11, 12,  # shoulders
    13, 14,  # elbows
    15, 16,  # wrists
    23, 24,  # hips
    25, 26,  # knees
    27, 28   # ankles
]

BODY_CONNECTIONS = frozenset([
    (11, 13), (13, 15),  # Left arm
    (12, 14), (14, 16),  # Right arm
    (11, 12),            # Shoulders
    (11, 23), (12, 24),  # Torso
    (23, 24),            # Hips
    (23, 25), (25, 27),  # Left leg
    (24, 26), (26, 28)   # Right leg
])

# # Open video file
# cap = cv2.VideoCapture('dance.mp4')
# if not cap.isOpened():
#     print("Error: Could not open video file.")
#     exit()

# # Open webcam with error checking
cap = cv2.VideoCapture(3)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

def calculate_angle_to_vertical(a, b):
    """
    Calculate the angle between a vector (defined by points a and b) and the vertical line
    Returns angle in degrees (0-360)
    """
    a = np.array(a[:2])
    b = np.array(b[:2])
    vector = b - a
    angle = np.degrees(np.arctan2(vector[0], -vector[1]))
    angle = angle % 360
    return angle

def map_angle_to_servo(angle, joint_type):
    """
    Map the calculated angle to the servo's range using offset and scale adjustments
    """
    adjusted_angle = (angle - 180)  # Basic mapping as before
    
    # Apply adjustments
    if joint_type in SERVO_ADJUSTMENTS:
        adjusted_angle = (adjusted_angle * SERVO_ADJUSTMENTS[joint_type]['scale'] + 
                         SERVO_ADJUSTMENTS[joint_type]['offset'])
    
    return adjusted_angle

def draw_angle_label(frame, joint_point, angle, joint_name=""):
    """
    Draw just the angle value and joint name at the joint location
    """
    x = int(joint_point[0])
    y = int(joint_point[1])
    cv2.putText(frame, f"{joint_name}: {angle:.1f}", 
                (x + 10, y + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

# Modify the main loop to include visualization
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Unable to read from video. Exiting...")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(frame_rgb)

    if result.pose_landmarks:
        h, w, c = frame.shape
        landmarks = result.pose_landmarks.landmark

        # Draw landmarks and connections
        for landmark_idx in BODY_LANDMARKS:
            landmark = landmarks[landmark_idx]
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            
        for connection in BODY_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            start_landmark = landmarks[start_idx]
            end_landmark = landmarks[end_idx]
            
            start_point = (int(start_landmark.x * w), int(start_landmark.y * h))
            end_point = (int(end_landmark.x * w), int(end_landmark.y * h))
            cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

        # Get points and calculate angles (keep your existing code)
        left_shoulder = [landmarks[11].x * w, landmarks[11].y * h]
        right_shoulder = [landmarks[12].x * w, landmarks[12].y * h]
        left_elbow = [landmarks[13].x * w, landmarks[13].y * h]
        right_elbow = [landmarks[14].x * w, landmarks[14].y * h]
        left_wrist = [landmarks[15].x * w, landmarks[15].y * h]
        right_wrist = [landmarks[16].x * w, landmarks[16].y * h]

        # Calculate angles
        left_bicep_angle = calculate_angle_to_vertical(left_shoulder, left_elbow)
        right_bicep_angle = calculate_angle_to_vertical(right_shoulder, right_elbow)
        left_forearm_angle = calculate_angle_to_vertical(left_elbow, left_wrist)
        right_forearm_angle = calculate_angle_to_vertical(right_elbow, right_wrist)

        # Draw angle labels
        draw_angle_label(frame, left_shoulder, left_bicep_angle, "left_bicep_angle")
        draw_angle_label(frame, right_shoulder, right_bicep_angle, "right_bicep_angle")
        draw_angle_label(frame, left_elbow, left_forearm_angle, "left_forearm_angle")
        draw_angle_label(frame, right_elbow, right_forearm_angle, "right_forearm_angle")

        # Your existing robot control code...
        try:
            right_shoulder_angle = map_angle_to_servo(right_bicep_angle, 'right_shoulder')
            print(f"Right shoulder angle: {right_shoulder_angle}")
            right_elbow_angle = map_angle_to_servo(right_forearm_angle, 'right_elbow')
            robot.servo.set_position(SERVO_MAPPING['right_shoulder'], right_shoulder_angle)
            robot.servo.set_position(SERVO_MAPPING['right_elbow'], right_elbow_angle)

            left_shoulder_angle = map_angle_to_servo(left_bicep_angle, 'left_shoulder')
            left_elbow_angle = map_angle_to_servo(left_forearm_angle, 'left_elbow')
            robot.servo.set_position(SERVO_MAPPING['left_shoulder'], left_shoulder_angle)
            robot.servo.set_position(SERVO_MAPPING['left_elbow'], left_elbow_angle)

        except Exception as e:
            print(f"Error sending commands to robot: {e}")

    cv2.imshow("Pose Detection", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
