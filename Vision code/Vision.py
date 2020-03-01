from GrassRemover import GrassRemover
from Detection import Detect
import cv2 as cv
import numpy as np
import datetime
import datetime
import tesserocr
from tesserocr import PyTessBaseAPI, PSM
from os.path import dirname, abspath
#################
# Video loading #
#################
# Using file
#cap = cv.VideoCapture(dirname(dirname(dirname(abspath(__file__)))) + '/VisionSample/New (1).mp4')

# Using webcam
cap = cv.VideoCapture(0)

# Using RTSP
#cap = cv.VideoCapture("rtsp://192.168.42.1/live")

# Using RTSP that doesn't work
#cap = cv.VideoCapture(
#    "rtspsrc location=rtsp://192.168.42.1/live ! appsink max-buffers=1 drop=true")

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

#############
# Main code #
#############

# Open Tesseract api
# With Page Seperation Mode as Single Character
# And englimg lgrayguage
with PyTessBaseAPI(path=dirname(dirname(dirname(abspath(__file__)))) + '/tessdata_fast-master', psm=PSM.SINGLE_CHAR, lang='eng') as api:
    # Only look for alpha numerics
    api.SetVariable('tessedit_char_whitelist',
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    # MarkerGroups
    markerGroups = []

    # Read until video is completed
    ret = True
    while (True):
        # Drop frames, if needed
        # This shouldn't be necessarry if the code is fast enough
        #cap.grab()

        # Read the frame
        ret, frame = cap.read() 
        if (not ret):
            break
        # TODO This is pretty much just a waste of time, but it works
        # Copy the frame
        im = frame.copy()

        # Remove grass and grayscale image
        NoGrassGray = GrassRemover(frame)

        # Run detection
        # And measure the time it takes
        a = datetime.datetime.now()
        t = Detect(NoGrassGray, frame, api, markerGroups)
        b = datetime.datetime.now()
        c = b - a
        #print("time", int(c.total_seconds() * 1000))

        #############
        ### DEBUG ###
        #############
        # Show original image
        #cv.imshow("Original", im)

        # Show image without grass
        cv.imshow("No Grass Image", NoGrassGray)

        # Show the Detect result
        cv.imshow("Detection", t)
     
        # Set this to:
        #  1: live video
        #  0: individual frames
        ch = cv.waitKey(1)
        # Quit if 'q' is pressed
        if ch & 0xFF == ord('q'):
            break
        
    # When everything done, release the video capture object
    cap.release()
