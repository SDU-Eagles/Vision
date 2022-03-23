import cv2
import numpy as np

# Number of contours
marker_identifiers = np.array([9, 1, 4, 4, 3])



def identify_marker(marker):    # TODO: Not done. Perimeter is a horrible measure for discrete edges.
    # area = 0
    # perimeter = 0

    # for contour in marker:
    #     area += cv2.contourArea(contour)
    #     perimeter += cv2.arcLength(contour, True)

    # if (area != 0 or perimeter != 0):
    #     ratio = area / perimeter

    #     idx = (np.abs(marker_identifiers - ratio)).argmin()
    #     markerID = idx + 1
        
    #     return markerID
    
    # else:
    #     return -1


    if (len(marker) != 0):        
        idx = (np.abs(marker_identifiers - len(marker))).argmin()
        markerID = idx + 1
        return markerID
    else:
        return -1