import cv2
import numpy as np


# Inversed covariance matrix and average from "colour_variance/get_threshold.py"
# Used to determine Mahalanobis distance for colour segmentation
cov_inv = np.array([[0.32621069, -0.3328852, 0.01422344],
                    [-0.3328852, 0.37590837, -0.03352803],
                    [0.01422344, -0.03352803, 0.01590636]])

avg = np.array([100.40176446, 92.74843263, 209.55799693])

# Area / Perimiter
marker_identifiers = np.array([50.09054353854687, 90.5906442250778, 80.15582483879922, 102.25, 202.03946401399423])



def detect_marker_contours(img):

    img = cv2.GaussianBlur(img, (3, 3), 0)
    
    pixels = np.reshape(img, (-1, 3))
    # segmented_image = mahalanobis(pixels, cov_inv, avg)
    segmented_image = cv2.inRange(img, (0, 0, 245), (10, 10, 256))  # Full marker image


    # Morphological filtering the image
    kernel_cls = np.ones((9, 9), np.uint8)
    morp_image = cv2.morphologyEx(segmented_image, cv2.MORPH_CLOSE, kernel_cls)

    contours, hierarchy = cv2.findContours(morp_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def group_contours(contours):   # TODO: Not done
    pass


def identify_marker(marker):
    area = 0
    perimeter = 0

    for contour in marker:
        area += cv2.contourArea(contour)
        perimeter += cv2.arcLength(contour, True)

    ratio = area / perimeter

    idx = (np.abs(marker_identifiers - ratio)).argmin()
    markerID = marker_identifiers[idx]
    
    return markerID


def locate_marker(marker):  # TODO: Not done
    markerLOC = [0, 0]

    return markerLOC


def mahalanobis(pixels, cov_inv, avg):
    # Mahalanobis based segmentation
    shape = pixels.shape
    diff = pixels - np.repeat([avg], shape[0], axis=0)

    mahalanobis_dist = np.sum(diff * (diff @ cov_inv), axis=1)
    mahalanobis_distance_image = np.reshape(mahalanobis_dist, (img.shape[0], img.shape[1]))

    _, mahalanobis_segmented = cv2.threshold(mahalanobis_distance_image, 40, 255, cv2.THRESH_BINARY_INV)
    mahalanobis_segmented = mahalanobis_segmented.astype(np.uint8)

    return mahalanobis_segmented



if __name__ == "__main__":

    # Load image
    path = "Markers/Marker5.png"
    # path = "Sample_images/5.jpg"
    img = cv2.imread(path)


    marker_contours = detect_marker_contours(img)
    # grouped_markers = group_contours(marker_contours)


    # for marker in grouped_markers:
    #     markerID,  = identify_marker(marker)
    #     markerLOC = locate_marker(marker)

    #     print(markerID, markerLOC)




    cv2.drawContours(image=img, contours=marker_contours, contourIdx=-1, color=(0, 255, 0), thickness=5, lineType=cv2.LINE_AA)
    height, width, channels = img.shape 
    dim = (600, round(600 * height/width))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)

    cv2.imshow('contours', img)
    cv2.waitKey(0)
