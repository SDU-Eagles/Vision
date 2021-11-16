import numpy as np
import cv2

path = "Markers/Marker1.png"
dim = (500, 500)
img = cv2.imread(path)
img = cv2.resize(img, dim, interpolation= cv2.INTER_LINEAR)
cv2.imshow('image', img)




cv2.waitKey(0)
