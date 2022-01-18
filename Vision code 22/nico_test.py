import cv2
from math import dist
import numpy as np

# path = "Markers/Marker1.png"
path = "Sample_images/5.jpg"
dim = (500, 500)
img = cv2.imread(path)
img = cv2.resize(img, dim, interpolation= cv2.INTER_LINEAR)


def inLabDist(img, colour, maxDist):

    # Convert to CieLAB
    colour = cv2.cvtColor( np.uint8([[colour]] ), cv2.COLOR_BGR2LAB)[0][0]
    mask = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Loop through image
    for i, row in enumerate(mask):
        for j, pixel in enumerate(row):
            distance = dist(colour, pixel)
            if (distance > maxDist):
                mask[i][j] = 0
            else:
                mask[i][j] = 255
    
    return mask[:,:,1]


def crop(bit_img):
    top = []
    left = []
    right = []
    bottom = []

    def get_top(): 
        for i, row in enumerate(bit_img):
            for j, pixel in enumerate(row):
                if (pixel != 0):
                    return [i,j]

    return get_top()


mask = inLabDist(img, [0, 0, 255], 80)
result = cv2.bitwise_and(img, img, mask = mask)

print(crop(mask))
# kernel = np.ones((4, 4), np.uint8)
# result = cv2.erode(result, kernel) 
# result = cv2.dilate(result, kernel)


cv2.imshow('image', result)
cv2.waitKey(0)
