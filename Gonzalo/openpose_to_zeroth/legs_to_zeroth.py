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
robot.servo.set_position(6, 5)

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
    'right_hip_yaw': 4,
    'right_knee': 2,
    'right_ankle': 1,
    'left_hip_yaw': 9,
    'left_knee': 7,
    'left_ankle': 6,
    'right_elbow': 11,
    'right_shoulder': 12,
    'left_shoulder': 15,
    'left_elbow': 16
}

#Servo ID to 0 is straight, 90 is backwards, -90 is forward


# Angle adjustment parameters for each servo
SERVO_ADJUSTMENTS = {
    'right_hip_yaw': {'offset': -45, 'scale': 1.5},
    'right_knee': {'offset': 50, 'scale': -1.0},
    'right_ankle': {'offset': 0, 'scale': 1.0},
    'left_hip_yaw': {'offset': 45, 'scale': 1.5},
    'left_knee': {'offset': -50, 'scale': -1.0},
    'left_ankle': {'offset': 0, 'scale': 1.0},
    'right_shoulder': {'offset': 50, 'scale': -1.0},
    'right_elbow': {'offset': -90, 'scale': 1.0},
    'left_shoulder': {'offset': -40, 'scale': -1.0},
    'left_elbow': {'offset': 90, 'scale': 1.0}
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

# Open webcam with error checking
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
    
    # Add safety limits
    if joint_type == 'right_hip_pitch':
        adjusted_angle = np.clip(adjusted_angle, -45, 45)
    elif joint_type == 'right_knee':
        adjusted_angle = np.clip(adjusted_angle, -90, 90)
    elif joint_type in ['right_ankle', 'left_ankle']:  # Added ankle limits
        adjusted_angle = np.clip(adjusted_angle, -90, 90)
    
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

        # Draw all MediaPipe landmarks and connections
        mp_drawing.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )

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

        # Get right leg points
        right_hip = [landmarks[24].x * w, landmarks[24].y * h]
        right_knee = [landmarks[26].x * w, landmarks[26].y * h]
        right_ankle = [landmarks[28].x * w, landmarks[28].y * h]

        # Calculate angles
        right_thigh_angle = calculate_angle_to_vertical(right_hip, right_knee)
        right_shin_angle = calculate_angle_to_vertical(right_knee, right_ankle)

        # Draw angle labels
        draw_angle_label(frame, right_hip, right_thigh_angle, "right_hip_angle")
        draw_angle_label(frame, right_knee, right_shin_angle, "right_knee_angle")

        # Get left leg points
        left_hip = [landmarks[23].x * w, landmarks[23].y * h]
        left_knee = [landmarks[25].x * w, landmarks[25].y * h]
        left_ankle = [landmarks[27].x * w, landmarks[27].y * h]

        # Calculate angles for left leg
        left_thigh_angle = calculate_angle_to_vertical(left_hip, left_knee)
        left_shin_angle = calculate_angle_to_vertical(left_knee, left_ankle)

        # Draw angle labels for left leg
        draw_angle_label(frame, left_hip, left_thigh_angle, "left_hip_angle")
        draw_angle_label(frame, left_knee, left_shin_angle, "left_knee_angle")

        # Get foot points
        right_foot = [landmarks[32].x * w, landmarks[32].y * h]
        left_foot = [landmarks[31].x * w, landmarks[31].y * h]

        # Right ankle - now using foot point instead of knee
        right_foot_angle = calculate_angle_to_vertical(right_ankle, right_foot)
        right_ankle_servo = map_angle_to_servo(right_foot_angle, 'right_ankle')

        # Left ankle - now using foot point instead of knee
        left_foot_angle = calculate_angle_to_vertical(left_ankle, left_foot)
        left_ankle_servo = map_angle_to_servo(left_foot_angle, 'left_ankle')

        # Add arm tracking
        left_shoulder = [landmarks[11].x * w, landmarks[11].y * h]
        right_shoulder = [landmarks[12].x * w, landmarks[12].y * h]
        left_elbow = [landmarks[13].x * w, landmarks[13].y * h]
        right_elbow = [landmarks[14].x * w, landmarks[14].y * h]
        left_wrist = [landmarks[15].x * w, landmarks[15].y * h]
        right_wrist = [landmarks[16].x * w, landmarks[16].y * h]

        # Calculate arm angles
        left_bicep_angle = calculate_angle_to_vertical(left_shoulder, left_elbow)
        right_bicep_angle = calculate_angle_to_vertical(right_shoulder, right_elbow)
        left_forearm_angle = calculate_angle_to_vertical(left_elbow, left_wrist)
        right_forearm_angle = calculate_angle_to_vertical(right_elbow, right_wrist)

        # Draw arm angle labels
        draw_angle_label(frame, left_shoulder, left_bicep_angle, "left_bicep_angle")
        draw_angle_label(frame, right_shoulder, right_bicep_angle, "right_bicep_angle")
        draw_angle_label(frame, left_elbow, left_forearm_angle, "left_forearm_angle")
        draw_angle_label(frame, right_elbow, right_forearm_angle, "right_forearm_angle")

        # Map angles to servo positions and send commands
        try:
            # Right leg (existing code)
            right_hip_yaw = map_angle_to_servo(right_thigh_angle, 'right_hip_yaw')
            right_knee_angle = map_angle_to_servo(right_shin_angle, 'right_knee')
            
            # Left leg (new code)
            left_hip_yaw = map_angle_to_servo(left_thigh_angle, 'left_hip_yaw')
            left_knee_angle = map_angle_to_servo(left_shin_angle, 'left_knee')
            
            # Add arm tracking
            right_shoulder_angle = map_angle_to_servo(right_bicep_angle, 'right_shoulder')
            right_elbow_angle = map_angle_to_servo(right_forearm_angle, 'right_elbow')
            left_shoulder_angle = map_angle_to_servo(left_bicep_angle, 'left_shoulder')
            left_elbow_angle = map_angle_to_servo(left_forearm_angle, 'left_elbow')

            # Print servo IDs and angles for both legs
            print("************************************************")
            print(f"Right Hip Yaw (ID {SERVO_MAPPING['right_hip_yaw']}): {right_hip_yaw:.2f}°")
            print(f"Right Knee (ID {SERVO_MAPPING['right_knee']}): {right_knee_angle:.2f}°")
            print(f"Right Ankle (ID {SERVO_MAPPING['right_ankle']}): {right_ankle_servo:.2f}°")
            print(f"Left Hip Yaw (ID {SERVO_MAPPING['left_hip_yaw']}): {left_hip_yaw:.2f}°")
            print(f"Left Knee (ID {SERVO_MAPPING['left_knee']}): {left_knee_angle:.2f}°")
            print(f"Left Ankle (ID {SERVO_MAPPING['left_ankle']}): {left_ankle_servo:.2f}°")
            print(f"Right Shoulder (ID {SERVO_MAPPING['right_shoulder']}): {right_shoulder_angle:.2f}°")
            print(f"Right Elbow (ID {SERVO_MAPPING['right_elbow']}): {right_elbow_angle:.2f}°")
            print(f"Left Shoulder (ID {SERVO_MAPPING['left_shoulder']}): {left_shoulder_angle:.2f}°")
            print(f"Left Elbow (ID {SERVO_MAPPING['left_elbow']}): {left_elbow_angle:.2f}°")
            
            # Send commands to robot for both legs
            robot.servo.set_position(SERVO_MAPPING['right_hip_yaw'], right_hip_yaw)
            robot.servo.set_position(SERVO_MAPPING['right_knee'], right_knee_angle)
            robot.servo.set_position(SERVO_MAPPING['left_hip_yaw'], left_hip_yaw)
            robot.servo.set_position(SERVO_MAPPING['left_knee'], left_knee_angle)
            robot.servo.set_position(SERVO_MAPPING['right_ankle'], right_ankle_servo)
            robot.servo.set_position(SERVO_MAPPING['left_ankle'], left_ankle_servo)
            robot.servo.set_position(SERVO_MAPPING['right_shoulder'], right_shoulder_angle)
            robot.servo.set_position(SERVO_MAPPING['right_elbow'], right_elbow_angle)
            robot.servo.set_position(SERVO_MAPPING['left_shoulder'], left_shoulder_angle)
            robot.servo.set_position(SERVO_MAPPING['left_elbow'], left_elbow_angle)

        except Exception as e:
            print(f"Error sending commands to robot: {e}")

    cv2.imshow("Pose Detection", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


time.sleep(0.01)

cap.release()
cv2.destroyAllWindows()
