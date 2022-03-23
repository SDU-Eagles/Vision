import cv2
import numpy as np

import scipy.cluster.hierarchy as shc
from matplotlib import pyplot as plt


# Inversed covariance matrix and average from "colour_variance/get_threshold.py"
# Used to determine Mahalanobis distance for colour segmentation
cov_inv = np.array([[0.32621069, -0.3328852, 0.01422344],
                    [-0.3328852, 0.37590837, -0.03352803],
                    [0.01422344, -0.03352803, 0.01590636]])

avg = np.array([100.40176446, 92.74843263, 209.55799693])



def show_image(img, contours):

    cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=5, lineType=cv2.LINE_AA)
    height, width, channels = img.shape 
    dim = (600, round(600 * height/width))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)

    cv2.imshow('contours', img)
    cv2.waitKey(0)


def mahalanobis(img, pixels, cov_inv, avg):
    # Mahalanobis based segmentation
    shape = pixels.shape
    diff = pixels - np.repeat([avg], shape[0], axis=0)

    mahalanobis_dist = np.sum(diff * (diff @ cov_inv), axis=1)
    mahalanobis_distance_image = np.reshape(mahalanobis_dist, (img.shape[0], img.shape[1]))

    _, mahalanobis_segmented = cv2.threshold(mahalanobis_distance_image, 40, 255, cv2.THRESH_BINARY_INV)
    mahalanobis_segmented = mahalanobis_segmented.astype(np.uint8)

    return mahalanobis_segmented


def group_contours(contours):   # TODO: Not done. Hierarchical Clustering? K-means? Gaussian Mixture Model?
    # Output: Array of markers, consisting of multiple contours
    
    contour_moments = []

    for contour in contours:
        M = cv2.moments(contour)
        
        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            contour_moments.append([cx, cy])


    dend = shc.dendrogram(shc.linkage(contour_moments, method='single'))
    # plt.show()



    return np.array([contours], dtype=object)


def detect_marker_contours(img, debug = False, img_is_groundtruth = False):

    img = cv2.GaussianBlur(img, (3, 3), 0)
    
    pixels = np.reshape(img, (-1, 3))

    if (img_is_groundtruth):
        segmented_image = cv2.inRange(img, (0, 0, 245), (10, 10, 256))  # Full marker image (completely red)
    else:
        segmented_image = mahalanobis(img, pixels, cov_inv, avg)


    # Morphological filtering the image
    kernel_cls = np.ones((9, 9), np.uint8)
    morp_image = cv2.morphologyEx(segmented_image, cv2.MORPH_CLOSE, kernel_cls)

    contours, hierarchy = cv2.findContours(morp_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    approx_contours = []

    for contour in contours:
        hull = cv2.convexHull(contour)
        approx_contours.append(hull)


    grouped_markers = group_contours(approx_contours)


    if (debug):
        if (len(approx_contours) == 0):
            print("No markers found!")

        show_image(img, approx_contours)


    return grouped_markers




if __name__ == "__main__":

    # Load image
    # path = "Markers/Marker5.png"
    path = "Sample_images/9.jpg"
    img = cv2.imread(path)


    marker_contours = detect_marker_contours(img, debug = True, img_is_groundtruth = False)
