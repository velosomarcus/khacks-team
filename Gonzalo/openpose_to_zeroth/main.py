import cv2
import mediapipe as mp
import csv
import time
import numpy as np
import math

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)
mp_drawing = mp.solutions.drawing_utils

# Define the body landmarks we want to keep (excluding face and hands)
BODY_LANDMARKS = [
    11, 12,  # shoulders
    13, 14,  # elbows
    15, 16,  # wrists
    23, 24,  # hips
    25, 26,  # knees
    27, 28   # ankles
]

# Define custom connections for body only
BODY_CONNECTIONS = frozenset([
    (11, 13), (13, 15),  # Left arm
    (12, 14), (14, 16),  # Right arm
    (11, 12),            # Shoulders
    (11, 23), (12, 24),  # Torso
    (23, 24),            # Hips
    (23, 25), (25, 27),  # Left leg
    (24, 26), (26, 28)   # Right leg
])

# Open CSV file
csv_file = open('pose_landmarks.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

# Write header
header = ['timestamp']
for i in BODY_LANDMARKS:
    header.extend([f'landmark_{i}_x', f'landmark_{i}_y', f'landmark_{i}_z'])
header.extend(['left_forearm_angle', 'right_forearm_angle', 
              'left_bicep_angle', 'right_bicep_angle'])
csv_writer.writerow(header)

#This is to use webcam, I've commented it out to read dance.mp4 instead for now.
# # Open webcam with error checking
# cap = cv2.VideoCapture(3)
# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# Open video file with error checking
cap = cv2.VideoCapture('dance.mp4')
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

def calculate_angle_to_vertical(a, b):
    """
    Calculate the angle between a vector (defined by points a and b) and the vertical line
    Returns angle in degrees (0-360), measured counter-clockwise from vertical down:
    - 0 degrees = vertical down
    - 90 degrees = horizontal right
    - 180 degrees = vertical up
    - 270 degrees = horizontal left
    """
    a = np.array(a[:2])  # Only use x,y coordinates
    b = np.array(b[:2])
    
    # Calculate vector
    vector = b - a
    
    # Calculate angle with respect to vertical (negative y-axis)
    angle = np.degrees(np.arctan2(vector[0], -vector[1]))
    
    # Convert to 0-360 range
    angle = angle % 360
    
    return angle

def draw_angle_label(frame, joint_point, angle, joint_name=""):
    """
    Draw just the angle value and joint name at the joint location
    """
    # Convert joint point to integers
    x = int(joint_point[0])
    y = int(joint_point[1])
    
    # Add text label without degree symbol
    cv2.putText(frame, f"{joint_name}: {angle:.1f}", 
                (x + 10, y + 10),  # Offset text slightly from joint
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Unable to read from webcam. Exiting...")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(frame_rgb)

    if result.pose_landmarks:
        # Draw body landmarks and connections (keep your existing visualization code)
        for landmark_idx in BODY_LANDMARKS:
            landmark = result.pose_landmarks.landmark[landmark_idx]
            h, w, c = frame.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            
        for connection in BODY_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            start_landmark = result.pose_landmarks.landmark[start_idx]
            end_landmark = result.pose_landmarks.landmark[end_idx]
            
            h, w, c = frame.shape
            start_point = (int(start_landmark.x * w), int(start_landmark.y * h))
            end_point = (int(end_landmark.x * w), int(end_landmark.y * h))
            cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

        # Calculate angles
        h, w, c = frame.shape
        landmarks = result.pose_landmarks.landmark
        
        # Get points for angle calculation
        left_shoulder = [landmarks[11].x * w, landmarks[11].y * h]
        right_shoulder = [landmarks[12].x * w, landmarks[12].y * h]
        left_elbow = [landmarks[13].x * w, landmarks[13].y * h]
        right_elbow = [landmarks[14].x * w, landmarks[14].y * h]
        left_wrist = [landmarks[15].x * w, landmarks[15].y * h]
        right_wrist = [landmarks[16].x * w, landmarks[16].y * h]

        # Calculate angles relative to vertical
        left_bicep_angle = calculate_angle_to_vertical(left_shoulder, left_elbow)
        right_bicep_angle = calculate_angle_to_vertical(right_shoulder, right_elbow)
        left_forearm_angle = calculate_angle_to_vertical(left_elbow, left_wrist)
        right_forearm_angle = calculate_angle_to_vertical(right_elbow, right_wrist)

        # Draw angle labels
        draw_angle_label(frame, left_shoulder, left_bicep_angle, "left_bicep_angle")
        draw_angle_label(frame, right_shoulder, right_bicep_angle, "right_bicep_angle")
        draw_angle_label(frame, left_elbow, left_forearm_angle, "left_forearm_angle")
        draw_angle_label(frame, right_elbow, right_forearm_angle, "right_forearm_angle")

        # Save data to CSV
        timestamp = time.time()
        row_data = [timestamp]
        
        # Save landmark data
        for idx in BODY_LANDMARKS:
            landmark = result.pose_landmarks.landmark[idx]
            row_data.extend([landmark.x, landmark.y, landmark.z])
        
        # Add angles to row data
        row_data.extend([left_forearm_angle, right_forearm_angle, 
                        left_bicep_angle, right_bicep_angle])
        
        csv_writer.writerow(row_data)

    cv2.imshow("Pose Detection", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
csv_file.close()
