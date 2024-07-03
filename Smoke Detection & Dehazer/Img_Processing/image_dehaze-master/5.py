import cv2
import pyautogui
import numpy as np

# Get the screen width and height
screen_width, screen_height = pyautogui.size()

# Set the region to capture (in this example, capture the entire screen)
capture_region = (0, 0, screen_width, screen_height)

# Create a VideoCapture object for screen capturing
screen_capture = cv2.VideoCapture(0)

while True:
    # Capture a screenshot using pyautogui
    screenshot = pyautogui.screenshot(region=capture_region)

    # Convert the screenshot to a NumPy array
    frame = np.array(screenshot)

    # Convert the BGR image to RGB (OpenCV uses BGR by default)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the captured screen in an OpenCV window
    cv2.imshow('Screen Capture', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the screen capture object and close the OpenCV window
screen_capture.release()
cv2.destroyAllWindows()
