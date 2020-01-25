import cv2
import numpy as np

class Marker:
    ######################
    # External Variables #
    ######################
    # Marker ocr size
    msize = 20

    ######################
    # Internal Variables #
    ######################
    # Center of the marker
    # Not in use
    center = (0,0)
    # The registered score of the marker
    score = 0
    # The original contour defining the marker
    c = None
    # An approximate poly describing c
    approx = None
    # Min area rectangle of the contour
    r = None
    # The projection square
    psqr = np.float32(
        [[0, 0], [msize, 0], [0, msize], [msize, msize]])

    def __init__(self, c, approx):
        self.c = c
        self.approx = approx
        self.r = cv2.minAreaRect(approx)

    def getScore(self):
        # Get min area rectangle
        r = cv2.minAreaRect(self.approx)
        (x, y), (width, height), angle = r

        # Calculate aspect ratio
        aspectRatio = min(width, height) / max(width, height)
        # Use it to calculate score
        self.score += aspectRatio * 100

        # Compute the solidity of the original contour
        # TODO Change this to use convex hull and min area rect
        area = cv2.contourArea(self.c)
        hullArea = cv2.contourArea(cv2.convexHull(self.c))
        solidity = area / float(hullArea)
        rarea = float(width * height)
        squareness = min(area,rarea) / max(area,rarea)
        # Use it to calculate score
        self.score += squareness * 100
        self.score += solidity * 100

        # Ignore smaller squares
        if (width < 25 or height < 25):
            self.score -= 1000

        print(self.score, aspectRatio, solidity, squareness)
        return self.score

    def getProjMarker(self, im):
        # Get box points of min area rect
        k = cv2.boxPoints(self.r)

        # The corners of the marker
        pts = np.float32([k[3], k[0], k[2], k[1]])

        # Get transformation matrix and transform it on a n x n sqaure
        M = cv2.getPerspectiveTransform(pts, self.psqr)
        dst = cv2.warpPerspective(im, M, (20, 20))

        # Invert colors for better OCR result
        return cv2.bitwise_not(dst)

    # Draw the marker on img, with the score next to it
    def drawMarker(self, img, colour):
        # Draw rectangle around marker
        box = cv2.boxPoints(self.r) 
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, colour, 2)

        # Draw score
        (x, y), (width, height), angle = self.r
        cv2.putText(img, str(self.score), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, colour)

        # Return image with marker
        return img
