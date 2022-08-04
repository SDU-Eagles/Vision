import cv2

from detect_marker import detect_markers, show_image
from identify_marker import identify_marker
from locate_marker import locate_marker


def resize_img(img):
    height, width, _ = img.shape 
    dim = (600, round(600 * height/width))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
    return img


def show_cutout(img, ulc, lrc):
    zoom_img = img[ulc[1]:lrc[1], ulc[0]:lrc[0]]
    show_image(zoom_img)



# Load image
# path = "Markers/Marker5.png"
path = "Sample_images/9.jpg"
img = cv2.imread(path)
img = resize_img(img)

# Detect marker areas
marker_area = detect_markers(img, debug = False, img_is_groundtruth = False)

show_image(img)

for area in marker_area:

    show_cutout(img, area[0], area[1])

    markerID = identify_marker(area)
    print('Marker ID: ', markerID)
