from PIL import Image
from numpy import asarray
original= Image.open('C:/Users/ARYAN/Downloads/image_dehaze-master/image_dehaze-master/image/15.png')

numpydataarray = asarray(original)

print("Type after conversion : ", type(numpydataarray))
