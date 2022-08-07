import cv2
import numpy as np

import camera_param_intrinsic

from square_response import square_response
from mark_markers import mark_markers
from identify_marker import identify_marker
from locate_marker import locate_marker


def resize_img(img, height_dim = 4608):
    height, width, _ = img.shape 
    dim = (round(height_dim * width/height), height_dim)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
    scale_factor = height_dim / height

    return img, scale_factor


# Expected marker size in image.
def marker_image_size(marker_world_size, altitude, focal_length):
    ratio = altitude / marker_world_size
    marker_image_size = focal_length * ratio    # TODO: Ratio is inverted, WHY does THIS WORK??
    # marker_image_size = (marker_world_size * focal_length) / altitude
    return marker_image_size


def rotate_image(image, angle, target):
    row, col, _ = image.shape
    rot_mat = cv2.getRotationMatrix2D(target, np.rad2deg(angle), 1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col, row))
    return new_image


def show_cutout(img, centre_point, angle, marker_size):
    i = centre_point[0]
    j = centre_point[1]
    
    ulc = (int(i - marker_size/2), int(j - marker_size/2))
    lrc = (int(i + marker_size/2), int(j + marker_size/2))
    
    img_rotate = rotate_image(img, angle, centre_point)
    
    img_zoom = img_rotate[ulc[1]:lrc[1], ulc[0]:lrc[0]]
    cv2.imshow('cutout', img_zoom)
    cv2.waitKey(0)



# Load image
path = "Markers/markers_rotated.png"
# path = "Sample_images/8-3.jpg"
img = cv2.imread(path)
img, scale_factor = resize_img(img, 600)


# Get marker information
world_marker_size = 50
altitide = 5
marker_image_size = np.ceil(marker_image_size(world_marker_size, altitide, camera_param_intrinsic.FOCAL_LENGTH_PX) * scale_factor)

# Detect markers
response, gradient_angles = square_response(img, marker_image_size, debug = True)
marker_locations, marker_rotations = mark_markers(img, response, gradient_angles, marker_image_size, scale_factor, debug = True)

print("Number of found markers: ", len(marker_locations))


for location, angle in zip(marker_locations, marker_rotations):
    print(np.rad2deg(angle))
    # show_cutout(img, location, angle, marker_image_size)

#     markerID = identify_marker(location)
#     print('Marker ID: ', markerID)

