import cv2
import numpy as np

import camera_param_intrinsic

from square_response import square_response
from mark_markers import mark_markers
from identify_marker import identify_marker
from locate_marker import locate_marker

'''
TODO: 
- All kernels are scaled with scale_factor, however some must be an uneven number (not all?), 
which is not gaurenteed to be the case as of now.
- This algorithm is very sensitive to altitude/scale, especially if the middlepoint is not exact

Tuneable parameters:
    vision_main.py
    - Image size
    mark_markers.py
    - VALUE_THRESHOLD: How intese the response should be to be accepted
    - DISTANCE_THRESHOLD: How close points can be to be considered part of the same marker
    - MIN_RESPONSE_POINTS: The least amount of points in a cluster, that can be considered a marker
    - VAR_THRESHOLD: Variance threshold for circular mean problem (calculate average angle)
    identify_marker.py
    - EQUAL_THRESHOLD: How many gridpoints should match between marker and patterns, to consider it a match
'''

# Draw debug info onto image
def debug_info_img(img, location, angle, markerID, marker_size, scale_factor):
    color = np.random.randint(256, size=3)
    color = (int(color[0]), int(color[1]), int(color[2]))
    
    # Middle point
    # cv2.circle(img, location, int(20*scale_factor), (200,200,255), -1)
    # Rectangle around marker
    rot_rectangle = (location, (marker_size, marker_size), np.rad2deg(angle))
    box = cv2.boxPoints(rot_rectangle) 
    box = np.int0(box)  # Convert into integer values
    img = cv2.drawContours(img, [box], 0, color, int(np.ceil(5*scale_factor)))
    # Angle of marker
    eol_point = (int(np.cos(angle)*200*scale_factor)+location[0], int(np.sin(angle)*200*scale_factor)+location[1])
    cv2.line(img, location, eol_point, color, int(np.ceil(5*scale_factor)))
    # Marker ID by marker
    text = "ID: " + str(markerID) + ", angle: " + str(int(np.round(np.rad2deg(angle)))) + "[deg]"
    cv2.putText(img, text, eol_point, cv2.FONT_HERSHEY_SIMPLEX, 4*scale_factor, color, int(np.ceil(8*scale_factor)), cv2.LINE_AA)
    
    cv2.imwrite("output/debug_info.png", img)


def resize_img(img, height_dim = 4608):
    height, width, _ = img.shape 
    dim = (round(height_dim * width/height), height_dim)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
    scale_factor = height_dim / height

    return img, scale_factor


# Expected marker size in image.
def marker_image_size(marker_world_size, altitude, focal_length):
    marker_image_size = (marker_world_size * focal_length) / altitude
    return marker_image_size


def rotate_image(image, angle, target):
    row, col, _ = image.shape
    rot_mat = cv2.getRotationMatrix2D(target, np.rad2deg(angle), 1.0) 
    new_image = cv2.warpAffine(image, rot_mat, (col, row))
    return new_image


def marker_cutout(img, centre_point, angle, marker_size, debug=False):
    i = centre_point[0]
    j = centre_point[1]
    
    ulc = (int(i - marker_size/2), int(j - marker_size/2))
    lrc = (int(i + marker_size/2), int(j + marker_size/2))
    
    img_rotate = rotate_image(img, angle, centre_point)
    img_zoom = img_rotate[ulc[1]:lrc[1], ulc[0]:lrc[0]]
    
    if debug:
        cv2.imshow('cutout', img_zoom)
        cv2.waitKey(0)
    
    return img_zoom



# Load image
# path = "Markers/markers_rotated.png"
path = "Sample_images/img_2.jpg"
img = cv2.imread(path)
# img, scale_factor = resize_img(img, 1000)
scale_factor = 1


# Get marker information
grid_size = 5
world_marker_size = 0.5
altitide = 40
marker_image_size = marker_image_size(world_marker_size, altitide, camera_param_intrinsic.FOCAL_LENGTH_PX)
marker_image_size = np.ceil(marker_image_size * scale_factor)

# Detect markers
response, gradient_angles = square_response(img, marker_image_size, debug = True)
marker_locations, marker_rotations = mark_markers(img, response, gradient_angles, marker_image_size, scale_factor, debug = False)

print(f"Found {len(marker_locations)} markers")

img_marked = img.copy()

for location, angle in zip(marker_locations, marker_rotations):
    cutout = marker_cutout(img, location, angle, marker_image_size, debug = False)

    markerID = identify_marker(cutout, grid_size, scale_factor, debug = True)
    debug_info_img(img_marked, location, angle, markerID, marker_image_size, scale_factor)


print("Wrote image to path: 'output/debug_info.png'")
