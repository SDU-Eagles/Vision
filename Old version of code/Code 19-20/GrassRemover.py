#! /usr/bin/python3

import cv2 as cv
import numpy as np
import time

###################################################################################################

# Use HSV Color Space to remove the Green areas in the image
def GrassRemover(im):

    # Convert the original image to greyscale
    gim = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

    # Convert the Image to the HSV Color Space
    HSV = cv.cvtColor(im, cv.COLOR_BGR2HSV)

    # Split the image into H, S, V to filter each compontent seperately
    hsv = cv.split(HSV)

    # Delete pixels with high saturation values 
    thr, NoGrass = cv.threshold(hsv[1], 50, 255, cv.THRESH_BINARY_INV)

    # Delete the grass from the grayscale image
    NoGrassGray = cv.bitwise_and(NoGrass, gim)

    '''
    cv.namedWindow("h", cv.WINDOW_NORMAL)
    cv.imshow("h", hsv[0])

    cv.namedWindow("s", cv.WINDOW_NORMAL)
    cv.imshow("s", NoGrassGray)

    cv.namedWindow("v", cv.WINDOW_NORMAL)
    cv.imshow("v", hsv[2])
    cv.waitKey()
    '''

    return NoGrassGray

###################################################################################################

if (__name__ == '__main__'):

    # Load the video
    cap = cv.VideoCapture('../VisionSample/New1.mp4')

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
        
        cv.namedWindow("Original Image", cv.WINDOW_NORMAL)
        cv.imshow("Original Image", im)

        cv.namedWindow("No Grass Image", cv.WINDOW_NORMAL)
        cv.imshow("No Grass Image", NoGrassGray)
        
        ch = cv.waitKey(30)
        if ch & 0xFF == ord('q'):
            break

    # When everything done, release the video capture object
    cap.release()