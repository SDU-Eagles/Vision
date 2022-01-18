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


# Can be integrated in the inLabDist function, to reduce number og loops through image
def crop(img, bit_img):
    top = -1
    left = -1
    right = -1
    bottom = -1


    for i, row in enumerate(bit_img):
        for j, pixel in enumerate(row):
            if (pixel != 0):
                if (i < top or top == -1): top = i
                if (i > bottom or bottom == -1): bottom = i
                if (j < left or left == -1): left = j
                if (j > right or right == -1): right = j

    print(top, bottom, left, right)

    return img[top:bottom, left:right]


mask = inLabDist(img, [0, 0, 255], 80)
result = cv2.bitwise_and(img, img, mask = mask)
result_crop = crop(result, mask)

# kernel = np.ones((4, 4), np.uint8)
# result = cv2.erode(result, kernel) 
# result = cv2.dilate(result, kernel)

cv2.imshow('image', result_crop)
cv2.waitKey(0)
