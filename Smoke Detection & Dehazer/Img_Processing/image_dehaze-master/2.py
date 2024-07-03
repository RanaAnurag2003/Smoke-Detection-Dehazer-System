# # importing the modules needed
# import cv2
# import numpy as np
#
# # Reading the image
# image = cv2.imread('C:/Users/Yoyob/Desktop/Projects AIML23/Img_Processing/image_dehaze-master/image/15.jpg')
#
# # Creating the kernel(2d convolution matrix)
# kernel1 = np.ones((5, 5), np.float32)/30
#
# # Applying the filter2D() function
# img = cv2.filter2D(src=image, ddepth= -8, kernel=kernel1)
#
# # Shoeing the original and output image
# cv2.imshow('Original', image)
# cv2.imshow('Kernel Blur', img)
#
# cv2.waitKey()
# cv2.destroyAllWindows()

import cv2
from matplotlib import pyplot as plt
import numpy as np


def depthFilter(img):
    kernel = np.ones((5, 5), np.float32) / 25
    dst = cv2.filter2D(img, -1, kernel)
    plt.subplot(121), plt.imshow(img), plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(dst), plt.title('Averaging')
    plt.xticks([]), plt.yticks([])
    plt.show()


fn = 'C:/Users/Yoyob/Desktop/Projects AIML23/Img_Processing/image_dehaze-master/image/15.jpg'
src = cv2.imread(fn)
depthFilter(src)
