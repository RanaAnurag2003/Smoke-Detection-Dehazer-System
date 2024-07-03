import cv2
import numpy as np
# import adaptiveFilter

def dehaze(image, omega= 0.7, t_min=0.1):
    # Step 1: Calculate the dark channel of the input image
    min_channel = np.min(image, axis=2)

    # Step 2: Estimate the atmospheric light
    top_percentage = int(image.size * (1 - omega))
    flat_dark_channel = np.sort(min_channel.ravel())[:top_percentage]
    A = np.mean(flat_dark_channel)

    # Step 3: Estimate the transmission map
    transmission = 1 - omega * min_channel / A
    transmission = np.maximum(transmission, t_min)  # Clamp transmission to avoid division by zero

    # Step 4: Perform atmospheric scattering correction
    dehazed_image = np.zeros_like(image, dtype=np.uint8)
    for channel in range(3):
        dehazed_image[:, :, channel] = ((image[:, :, channel] - A) / transmission + A).clip(0, 255)

    return dehazed_image

# Load the hazy image
hazy_image = cv2.imread("C:/Users/Yoyob/Desktop/Projects AIML23/Img_Processing/image_dehaze-master/image/2.jpg")

# Dehaze the image (apply the depth filter)
dehazed_image = dehaze(hazy_image)

# Display or save the dehazed image
cv2.imshow("Dehazed Image", dehazed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
