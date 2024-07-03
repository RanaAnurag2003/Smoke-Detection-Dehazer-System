import cv2
import socket
import numpy as np

# Server address and port
SERVER_HOST = ' 172.21.231.131'  # Replace with the IP address of your server
SERVER_PORT = 6749            # Replace with the port your server is listening on

# Create a socket to connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

while True:
    try:
        # Receive the screen data from the server
        data = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet: break
            data += packet

        # Decode and display the screen
        frame = cv2.imdecode(np.frombuffer(data, np.uint8), -1)
        cv2.imshow("Screen Sharing", frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) == ord('q'):
            break

    except Exception as e:
        print(f"Error receiving data from the server: {e}")
        break

# Cleanup
cv2.destroyAllWindows()
client_socket.close()
