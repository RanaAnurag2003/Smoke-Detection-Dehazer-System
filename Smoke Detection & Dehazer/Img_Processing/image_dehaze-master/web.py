import cv2
import pyautogui
import numpy as np
from flask import Flask, Response

app = Flask(__name__)

# Set the screen size and frame rate
screen_width, screen_height = pyautogui.size()
frame_rate = 30

# Initialize the screen capture
screen_capture = pyautogui.screenshot()


def generate_frames():
    while True:
        # Capture the screen
        screenCapture = pyautogui.screenshot()
        frame = np.array(screenCapture)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)

        # Yield the frame as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/')
def index():
    return "Streaming your screen over HTTP!"


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
