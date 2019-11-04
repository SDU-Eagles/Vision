from GrassRemover import GrassRemover
from Detection import Detect
import cv2 as cv
import numpy as np
import time
import os

# Load the video
videoLoad = 'v2'
cap = cv.VideoCapture('./VisionSample/' + videoLoad + '.mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Read until video is completed
ret = True
while(True):
    ret, frame = cap.read() 
    if (not ret):
        break
    im = frame.copy()

    NoGrassGray = GrassRemover(frame)
    
    cv.namedWindow("Original", cv.WINDOW_NORMAL)
    cv.imshow("Original", im)
    cv.namedWindow("No Grass Image", cv.WINDOW_NORMAL)
    cv.imshow("No Grass Image", NoGrassGray)
    cv.namedWindow("Detection", cv.WINDOW_NORMAL)
    cv.imshow("Detection", Detect(im))

    # Quit if 'q' is pressed
    ch = cv.waitKey(30)
    if ch & 0xFF == ord('q'):
        break
    # Pause if 'p' is pressed
    elif ch & 0xFF == ord('p'):
        cv.waitKey()
# When everything done, release the video capture object
cap.release()