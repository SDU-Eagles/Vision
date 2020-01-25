import cv2
import numpy as np
import pytesseract
from OCR import OCR
from Marker import Marker

def Detect(im, ref, api):
    # Blur image and detect edges
    edged = cv2.Canny(cv2.GaussianBlur(im, (9, 9), 0), 50, 150)
    
    # Find contours in the edge map
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(ref, cnts, -1, (0,255,0), 3)

    for c in cnts:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)

        # Ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 4 and len(approx) <= 6:
            m = Marker(c,approx)
            
            # Calculate score
            score = m.getScore()

            # Draw markers on image with score next to them
            #ref = m.drawMarker(ref, (0, 0, 255))

            # Temporary till marker class implemented
            if score > 270:
                # Run OCR 
                OCR(m.getProjMarker(im), api)

                ref = m.drawMarker(ref, (255, 0, 0))

                # TODO Remove when scoring system is done
                # Currently need to break
                # So it only runs OCR on one marker once
                #break
            
    # Return original image for debug purposes
    return ref
