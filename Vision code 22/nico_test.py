import cv2
from math import dist
import numpy as np

# path = "Markers/Marker1.png"
path = "hsv-colours.png"
dim = (500, 500)
img = cv2.imread(path)
img = cv2.resize(img, dim, interpolation= cv2.INTER_LINEAR)


def inLabDist(img, colour, maxDist):

    # Convert to CieLAB
    colour = cv2.cvtColor( np.uint8([[colour]] ), cv2.COLOR_BGR2LAB)[0][0]
    mask = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Loop throug image
    for i, row in enumerate(mask):
        for j, pixel in enumerate(row):
            distance = dist(colour, pixel)
            if (distance > maxDist):
                mask[i][j] = 0
            else:
                mask[i][j] = 255
    
    return mask



mask = inLabDist(img, [0, 0, 255], 100)
# result = cv2.bitwise_and(img, img, mask = mask)

cv2.imshow('image', mask)
cv2.waitKey(0)
