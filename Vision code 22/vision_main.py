import cv2
import numpy as np

from detect_marker import detect_marker_contours
from identify_marker import identify_marker
from locate_marker import locate_marker


# Load image
# path = "Markers/Marker5.png"
path = "Sample_images/5.jpg"
img = cv2.imread(path)


# Assuming only one marker present in image! TODO: Fix that (grouping and clustering)

marker_contours = detect_marker_contours(img, debug = False, img_is_groundtruth = False)

markerID = identify_marker(marker_contours)
print(markerID)

