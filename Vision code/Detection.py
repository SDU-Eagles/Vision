import cv2
import numpy as np
import pytesseract
from OCR import OCR
from Marker import Marker
from MarkerGroup import MarkerGroup

def Detect(gray, img, api, markerGroups):
    # List of detected and approved markers
    markers = []

    # Blur image and detect edges
    edged = cv2.Canny(cv2.GaussianBlur(gray, (9, 9), 0), 50, 150)
    
    # Find contours in the edge map
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Go through all detected contours
    for c in cnts:
        # Approximate the contour as polygon
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)

        # Ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 4 and len(approx) <= 6:
            # Create a marker instance
            m = Marker(c,approx)
            
            # Remove markers which are too bad to comply with the other rules
            if not m.valid(markers):
                continue

            # Calcaulate a quick score for the marker
            # And make sure it's good eneough for further testing
            if m.getScore() < 280:
                continue
            
            # Do further and more time heavy testing
            # And make sure the marker fulfulls these requirements
            if m.getSecondaryScore(img, gray) < 500:
                continue

            # Run OCR on a sqaure projection of the marker
            # TODO Ignore markers with zero confidence or length
            alphanum = OCR(m.getProjMarker(gray), api)

            b = True
            for mg in markerGroups:
                if mg.addMarker(m, alphanum):
                    b = False
            if b:
                markerGroups.append(MarkerGroup(m, alphanum))

            # Add marker to the list of approved markers
            markers.append(m)

    for mg in markerGroups:
        if not mg.tick():
            if (len(mg.markerList) <= 3):
                markerGroups.remove(mg)
                continue
            print(mg.color, mg.alphaNum)
            markerGroups.remove(mg)

    # Go through all approved markers
    for m in markers:
        # Get the color
        c = m.getColor()
        # And draw the marker on the image for debugging
        img = m.drawMarker(img, c, alphanum)

    #print(len(markerGroups))

    # Return original image for debug purposes
    return img
