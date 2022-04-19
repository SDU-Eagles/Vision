import cv2
import numpy as np

from detect_marker import detect_marker_contours
from identify_marker import identify_marker
from locate_marker import locate_marker


# Load image
# path = "Markers/Marker5.png"
path = "Sample_images/2.jpg"
img = cv2.imread(path)


# Assuming only one marker present in image! TODO: Fix that (grouping and clustering)

marker_contours = detect_marker_contours(img, debug = True, img_is_groundtruth = False)

for marker in marker_contours:
    markerID = identify_marker(marker)
    print(markerID)
