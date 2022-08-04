import cv2
import numpy as np

import camera_param_intrinsic

'''
TODO:
    - Change centre point identifier to choose mean, rather than simply highest value.
    - Handle multiple markers in one image.
    - Get rotation information
'''


# Expected marker size in image.
def marker_image_size(marker_world_size, altitude, focal_length):
    ratio = altitude / marker_world_size
    marker_image_size = focal_length * ratio    # TODO: Ratio is inverted, why does THIS WORK??
    # marker_image_size = (marker_world_size * focal_length) / altitude
    return marker_image_size


# Define area as two points for cv to draw (upper left corner, lower right corner)
def get_area_points(centre_point):
    
    marker_size = marker_image_size(50, 5, camera_param_intrinsic.FOCAL_LENGTH_PX)
    
    i = centre_point[0]
    j = centre_point[1]
    
    ulc = (int(i - marker_size/2), int(j - marker_size/2))
    lrc = (int(i + marker_size/2), int(j + marker_size/2))
    
    return ulc, lrc


# Define areas arond markers for identification and location.
def mark_markers(img, response, debug=False):
    
    img_marked = img.copy()
    markers = []
    highest_response = 0
    colour = 0
    
    for j, row in enumerate(response):
        for i, value in enumerate(row):
            if value > highest_response:
                
                cv2.circle(img_marked, (i,j), 10, (0,0,colour), -1)
                colour = colour + 1
                
                highest_response = value
                start_point, end_point = get_area_points((i, j))
                markers = [start_point, end_point, value]  # [ulc, lrc, value]

    print(markers)
    
    cv2.rectangle(img_marked, markers[0], markers[1], (0, 0, 255), 5)
    cv2.imwrite("output/mark_markers.png", img_marked)

        
    marker_areas = 0
    return marker_areas

