import cv2
import numpy as np
import pytesseract
from OCR import OCR

def Detect(im, ref, api):
    # Blur image and detect edges
    edged = cv2.Canny(cv2.GaussianBlur(im, (9, 9), 0), 50, 150)
    
    # Find contours in the edge map
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # DEBUG Draw all contours
    #cv2.drawContours(im, cnts, -1, (0, 255, 0), 4)

    for c in cnts:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)

        # Ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 4 and len(approx) <= 6:
            # Compute the bounding box of the approximated contour
            (x, y, w, h) = cv2.boundingRect(approx)

            # Get rectangle
            r = cv2.minAreaRect(approx)
            k = cv2.boxPoints(r)
            cv2.polylines(ref, np.int32([k]), True, (0, 255, 0))
            cv2.rectangle(ref, (x, y), (x + w, y + h), (255, 0, 0))

            # Calculate aspect ratio
            (x, y), (width, height), angle = r
            aspectRatio = min(width, height) / max(width, height)

            # Compute the solidity of the original contour
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)

            # TODO Rewrite this as a score function
            # Giving each contour a score
            # And assuming the highest score is correct
            # Currently it returns two contours for one marker

            # Compute whether or not the width and height, solidity, and
            # aspect ratio of the contour falls within appropriate bounds
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2
            
            # Calculate score
            score = aspectRatio * 100 + solidity * 100
            print (score)

            # ensure that the contour passes all our tests
            if keepDims and keepSolidity and keepAspectRatio:
                # Draw an outline around the target and update the status text
                cv2.drawContours(im, [approx], -1, (0, 0, 255), 4)
                #print('contour', approx)

                # TODO Make more efficient, this is also being done earlier
                # Get the corners of the marker
                r=cv2.minAreaRect(approx)
                k=cv2.boxPoints(r)
                
                # The corners of the marker
                pts1 = np.float32([k[3], k[0], k[2], k[1]])
                # TODO Make the size of the square a variable
                # TODO Probably dont need to create this every time
                # The projection square
                pts2 = np.float32([[0, 0], [20, 0], [0, 20], [20, 20]])

                # Get transformation matrix and transform it on a n x n sqaure
                M = cv2.getPerspectiveTransform(pts1, pts2)
                dst = cv2.warpPerspective(im, M, (20, 20))
				
                # Invert colors for better OCR result
                dst = cv2.bitwise_not(dst)
				
                # TODO Move this to the main function
                # Run OCR 
                OCR(dst, api)

                # Show the projected image of the marker
                cv2.imshow('cropppp', dst)
                cv2.imshow('cropppp', ref)

                # TODO Remove when scoring system is done
                # Currently need to break
                # So it only runs OCR on one marker once
                break
            
    # Return original image for no reason at all...
    return im
