import cv2
import mediapipe as mp
import csv
import time

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
csv_writer.writerow(header)

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

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Unable to read from webcam. Exiting...")
        break

    # Convert the frame to RGB (MediaPipe requires RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(frame_rgb)

    # Check for detected pose landmarks
    if result.pose_landmarks:
        # Create custom landmark drawing spec that only shows body landmarks
        landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
        connection_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
        
        # Draw only body landmarks and connections
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

        # Save only body landmarks to CSV
        timestamp = time.time()
        row_data = [timestamp]
        
        for idx in BODY_LANDMARKS:
            landmark = result.pose_landmarks.landmark[idx]
            row_data.extend([landmark.x, landmark.y, landmark.z])
            print(f"Landmark {idx}: x={landmark.x}, y={landmark.y}, z={landmark.z}")
        
        csv_writer.writerow(row_data)

    # Display the webcam feed with landmarks
    cv2.imshow("Pose Detection", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
csv_file.close()
