from GrassRemover import GrassRemover
from Detection import Detect
import cv2 as cv
import numpy as np
import time
import datetime
import tesserocr
from tesserocr import PyTessBaseAPI, PSM

# Load the video
cap = cv.VideoCapture('../../VisionSample/New (1).mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Open Tesseract api
# With Page Seperation Mode as Single Character
# And english language
with PyTessBaseAPI(path='../../tessdata_fast-master', psm=PSM.SINGLE_CHAR, lang='eng') as api:
    # Only look for Alpha Numeric
    # TODO This has some problems
    # Since it will still return non alphanumeric characters.
    api.SetVariable('tessedit_char_whitelist',
                        'ABCDEFGHIJKLMNOPQRSTUVXYZW1234567890')

    # Read until video is completed
    ret = True
    while (True):
        ret, frame = cap.read() 
        if (not ret):
            break
        # TODO Don't think this is actually needed
        # But it works so will change later
        im = frame.copy()

        # Remove grass and grayscale image
        NoGrassGray = GrassRemover(frame)

        # Calculate the time it takes to run detection
        # And currently also OCR
        a = datetime.datetime.now()
        t = Detect(NoGrassGray, frame, api)
        b = datetime.datetime.now()
        c = b - a
        print("time", int(c.total_seconds() * 1000))

        #############
        ### DEBUG ###
        #############
        # Show original image
        cv.namedWindow("Original", cv.WINDOW_NORMAL)
        cv.imshow("Original", im)
        # Show image without grass
        cv.namedWindow("No Grass Image", cv.WINDOW_NORMAL)
        cv.imshow("No Grass Image", NoGrassGray)
        # Show the Detect result
        # TODO This currently just returns the input image
        # While it should return the detection so OCR will be run in this file
        cv.namedWindow("Detection", cv.WINDOW_NORMAL)
        cv.imshow("Detection", t)

        # Quit if 'q' is pressed
        ch = cv.waitKey(1)
        if ch & 0xFF == ord('q'):
            break
        
    # When everything done, release the video capture object
    cap.release()
