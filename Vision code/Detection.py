import cv2
import numpy as np

def Detect(im):
    # Blur image
    blurred = cv2.GaussianBlur(im, (7, 7), 0)

    # Detect edges
    edged = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edge map
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw all contours
    cv2.drawContours(im, cnts, -1, (0, 255, 0), 4)

    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        # print (peri)
        # ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 4 and len(approx) <= 6:
            # compute the bounding box of the approximated contour and
            # use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)
            
            # compute the solidity of the original contour
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)

            # compute whether or not the width and height, solidity, and
            # aspect ratio of the contour falls within appropriate bounds
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

            # ensure that the contour passes all our tests
            if keepDims and keepSolidity and keepAspectRatio:
                # draw an outline around the target and update the status text
                cv2.drawContours(im, [approx], -1, (0, 0, 255), 4)
                print('contour', approx)
                # status = "Target(s) Acquired"

                r = cv2.minAreaRect(approx)
                k = cv2.boxPoints(r)
                pts1 = np.float32([k[3], k[0], k[2], k[1]])
                pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])

                M = cv2.getPerspectiveTransform(pts1, pts2)
                dst = cv2.warpPerspective(im, M, (300, 300))
                cv2.imshow('crop of detection', dst)

    return im