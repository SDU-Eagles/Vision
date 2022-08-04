from urllib import response
import cv2

from mark_markers import mark_markers
from square_response import square_response
from identify_marker import identify_marker
from locate_marker import locate_marker


def resize_img(img):
    height, width, _ = img.shape 
    dim = (600, round(600 * height/width))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
    return img


def show_cutout(img, ulc, lrc):
    zoom_img = img[ulc[1]:lrc[1], ulc[0]:lrc[0]]
    cv2.imshow('cutout', zoom_img)
    cv2.waitKey(0)



# Load image
# path = "Markers/Marker5.png"
path = "Sample_images/9.jpg"
img = cv2.imread(path)
# img = resize_img(img)



# Detect marker areas
response = square_response(img, debug = False)
marker_areas = mark_markers(img, response, debug = False)


cv2.imwrite("output/orig_main.png", img)
cv2.imwrite("output/square_response_main.png", response)

# for area in marker_areas:

#     show_cutout(img, area[0], area[1])

#     markerID = identify_marker(area)
#     print('Marker ID: ', markerID)
