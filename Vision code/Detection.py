import cv2
import numpy as np
import pytesseract
from OCR import OCR
from Marker import Marker

def Detect(gray, img, api):
    # Blur image and detect edges
    edged = cv2.Canny(cv2.GaussianBlur(gray, (9, 9), 0), 50, 150)
    
    # Find contours in the edge map
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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
            if score > 280:
                score = m.getSecondaryScore(img, gray)
                if score > 500:
                    # Run OCR 
                    improj = m.getProjMarker(gray)
                    #refproj = m.getProjMarker(img)

                    kernel = np.ones((2, 2), np.uint8)
                    improj = cv2.dilate(improj, kernel, iterations=1)

                    alphanum = OCR(improj, api)

                    #cv2.drawContours(ref, c, -1, (0, 255, 0), 3)
                    c = m.getColor() 

                    img = m.drawMarker(img, c, alphanum)

                    # TODO Remove when scoring system is done
                    # Currently need to break
                    # So it only runs OCR on one marker once
                    break
            
    # Return original image for debug purposes
    return img
