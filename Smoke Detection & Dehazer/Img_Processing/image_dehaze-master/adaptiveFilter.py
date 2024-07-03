import cv2
import numpy as np

# Load the hazy image
hazy_image = cv2.imread('C:/Users/Yoyob/Desktop/t4.jpg')

# Convert the image to float32 format
hazy_image = hazy_image.astype(np.float32) / 255.0

# Calculate the dark channel of the hazy image
dark_channel = np.min(hazy_image, axis=2)

# Estimate the atmospheric light
atmospheric_light = np.percentile(dark_channel, 95)

# Estimate the transmission map
omega = 0.95  # A constant to adjust the haze removal
transmission_map = 1 - omega * dark_channel / atmospheric_light

# Clamp the transmission map to avoid artifacts
transmission_map = np.clip(transmission_map, 0.1, 1.0)

# Perform guided filtering to refine the transmission map
# You may need to adjust the radius and epsilon parameters based on your image
radius = 40
epsilon = 0.001
guided_filter = cv2.ximgproc.createGuidedFilter(hazy_image, radius, epsilon)
refined_transmission_map = guided_filter.filter(transmission_map)

# Dehaze the image
dehazed_image = np.zeros_like(hazy_image)
for channel in range(3):
    dehazed_image[:, :, channel] = (hazy_image[:, :, channel] - atmospheric_light) / refined_transmission_map + atmospheric_light

# Clamp the dehazed image to the [0, 1] range
dehazed_image = np.clip(dehazed_image, 0, 1)

# Convert the dehazed image back to uint8 format
dehazed_image = (dehazed_image * 255).astype(np.uint8)

# Display the hazy and dehazed images
cv2.imshow('Hazy Image', hazy_image)
cv2.imshow('Dehazed Image', dehazed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
