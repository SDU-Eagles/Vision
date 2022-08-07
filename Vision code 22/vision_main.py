import cv2
import numpy as np

import camera_param_intrinsic

from square_response import square_response
from mark_markers import mark_markers
from identify_marker import identify_marker
from locate_marker import locate_marker


def resize_img(img):
    height, width, _ = img.shape 
    dim = (600, round(600 * height/width))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
    scale_factor = 600 / height
    return img, scale_factor


# Expected marker size in image.
def marker_image_size(marker_world_size, altitude, focal_length):
    ratio = altitude / marker_world_size
    marker_image_size = focal_length * ratio    # TODO: Ratio is inverted, WHY does THIS WORK??
    # marker_image_size = (marker_world_size * focal_length) / altitude
    return marker_image_size


def show_cutout(img, centre_point, marker_size):
    
    i = centre_point[0]
    j = centre_point[1]
    
    ulc = (int(i - marker_size/2), int(j - marker_size/2))
    lrc = (int(i + marker_size/2), int(j + marker_size/2))
    zoom_img = img[ulc[1]:lrc[1], ulc[0]:lrc[0]]
    cv2.imshow('cutout', zoom_img)
    cv2.waitKey(0)



# Load image
# path = "Markers/Marker5.png"
path = "Sample_images/9.jpg"
img = cv2.imread(path)
img, scale_factor = resize_img(img)

# Get marker information
world_marker_size = 50
altitide = 5
marker_image_size = np.ceil(marker_image_size(world_marker_size, altitide, camera_param_intrinsic.FOCAL_LENGTH_PX) * scale_factor)
print(marker_image_size)
# Detect markers
response, gradient_vectors = square_response(img, marker_image_size, debug = True)
marker_locations = mark_markers(img, response, marker_image_size, scale_factor, debug = True)

print("Number of found markers: ", len(marker_locations))


# for area in marker_locations:

#     show_cutout(img, area, marker_image_size)

#     markerID = identify_marker(area)
#     print('Marker ID: ', markerID)

