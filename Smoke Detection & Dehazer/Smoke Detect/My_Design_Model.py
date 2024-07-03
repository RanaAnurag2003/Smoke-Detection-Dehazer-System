import cv2
import os
import numpy as np

# Set the video source (0 for default camera)
video_source = 0

# Create a directory to store the captured frames and dehazed frames
input_directory = 'captured_frames'
output_directory = 'dehazed_frames'
os.makedirs(output_directory, exist_ok=True)

# Open a video capture object
cap = cv2.VideoCapture(video_source)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

frame_count = 0
frame_rate = 10  # Desired capture rate in FPS
frame_delay = int(1000 / frame_rate)  # Delay in milliseconds

def dehaze(frame):
    # Apply the Dark Channel Prior (DCP) algorithm for dehazing
    min_channel = np.minimum.reduce(frame, axis=2)
    dark_channel = cv2.erode(min_channel, np.ones((15, 15), np.uint8))
    atmospheric_light = np.max(frame, axis=(0, 1))
    transmission = 1 - 0.95 * dark_channel / np.max(atmospheric_light)  # Fix the atmospheric light calculation
    transmission = np.maximum(transmission, 0.1)  # Ensure minimum transmission
    dehazed_frame = np.empty_like(frame)
    for i in range(3):
        dehazed_frame[:, :, i] = (frame[:, :, i] - atmospheric_light[i]) / transmission + atmospheric_light[i]
    dehazed_frame = np.clip(dehazed_frame, 0, 255).astype(np.uint8)
    return dehazed_frame

while True:
    # Capture a frame from the video feed
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Save the original frame as an image file
    original_frame_filename = os.path.join(input_directory, f"frame_{frame_count:04d}.jpg")
    cv2.imwrite(original_frame_filename, frame)
    
    

    # Dehaze the frame
    dehazed_frame = dehaze(frame)

    # Save the dehazed frame as an image file
    dehazed_frame_filename = os.path.join(output_directory, f"dehazed_frame_{frame_count:04d}.jpg")
    cv2.imwrite(dehazed_frame_filename, dehazed_frame)

    # Display the dehazed frame (optional)
    cv2.imshow('Dehazed Frame', dehazed_frame)
    # Display the original frame (optional)
    cv2.imshow('Dehazed Frame', dehazed_frame)

    frame_count += 1

    # Delay to achieve the desired capture rate
    if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

