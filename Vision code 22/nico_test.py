import cv2
from math import dist
import numpy as np

# path = "Markers/Marker1.png"
path = "Sample_images/5.jpg"
img = cv2.imread(path)
height, width, channels = img.shape 
dim = (600, round(600 * height/width))
img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
pixels = np.reshape(img, (-1, 3))


# Inversed covariance matrix and average from "colour_variance/get_threshold.py"
# Used to determine Mahalanobis distance for colour segmentation
cov_inv = np.array([[0.32621069, -0.3328852, 0.01422344],
                    [-0.3328852, 0.37590837, -0.03352803],
                    [0.01422344, -0.03352803, 0.01590636]])

avg = np.array([100.40176446, 92.74843263, 209.55799693])



def inLabDist(img, colour, maxDist):

    # Convert to CieLAB
    colour = cv2.cvtColor( np.uint8([[colour]] ), cv2.COLOR_BGR2LAB)[0][0]
    mask = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Loop through image
    for i, row in enumerate(mask):
        for j, pixel in enumerate(row):
            distance = dist(colour, pixel)
            if (distance > maxDist):
                mask[i][j] = 255
            else:
                mask[i][j] = 0
    
    return mask[:,:,1]



# Can be integrated in the inLabDist function, to reduce number og loops through image
def crop(img):
    top = -1
    left = -1
    right = -1
    bottom = -1


    for i, row in enumerate(img):
        for j, pixel in enumerate(row):
            if (pixel != 0):
                if (i < top or top == -1): top = i
                if (i > bottom or bottom == -1): bottom = i
                if (j < left or left == -1): left = j
                if (j > right or right == -1): right = j

    return img[top:bottom, left:right]


# mask = inLabDist(img, [0, 0, 255], 80)
# print("mask")
# result = cv2.bitwise_and(img, img, mask = mask)
# print("result")
# result_crop = crop(result, mask)
# print("crop")
# edges = cv2.Canny(image=result_crop, threshold1=100, threshold2=200)
# print("edges")

# kernel = np.ones((4, 4), np.uint8)
# result = cv2.erode(result, kernel) 
# result = cv2.dilate(result, kernel)


def mahalanobis(pixels, cov_inv, avg):
    # Mahalanobis based segmentation
    shape = pixels.shape
    diff = pixels - np.repeat([avg], shape[0], axis=0)

    mahalanobis_dist = np.sum(diff * (diff @ cov_inv), axis=1)
    mahalanobis_distance_image = np.reshape(mahalanobis_dist, (img.shape[0], img.shape[1]))

    _, mahalanobis_segmented = cv2.threshold(mahalanobis_distance_image, 40, 255, cv2.THRESH_BINARY_INV)
    mahalanobis_segmented = mahalanobis_segmented.astype(np.uint8)

    return mahalanobis_segmented


segmented_image = mahalanobis(pixels, cov_inv, avg)
edges = cv2.Canny(image=segmented_image, threshold1=100, threshold2=200)

contours, hierarchy = cv2.findContours(segmented_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(img, contours, 0, (0,255,0), 2)
cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)


cv2.imshow('mahalanobis', segmented_image)
cv2.imshow('contours', img)
cv2.waitKey(0)
