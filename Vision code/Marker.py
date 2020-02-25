import cv2
import numpy as np
from sklearn.cluster import KMeans

class Marker:
    #############
    # Variables #
    #############
    # Marker ocr size
    msize = 40

    # Cutoff sides of projection
    sco = 4


    ####################
    # System variables #
    ####################

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
    # Dominant hue
    dhue = None

    def __init__(self, c, approx):
        self.c = c
        self.approx = approx
        self.r = cv2.minAreaRect(approx)

    # Makes sure the marker fulfills some minimum requirements like
    #  - Marker has not been detected before
    #  - Marker is not too small
    def valid(self, markers):
        # Get values from minAreaRect
        (x, y), (width, height), angle = self.r

        # Ignore smaller squares
        if (width < 25 or height < 25): 
            return False

        # Make sure the marker is not inside an already existing marker
        for m in markers:
            (mx, my), (mwidth, mheight), _ = m.r
            if (mx - mwidth/2 <= x <= mx + mwidth/2):
                return False
            if (my - mheight/2 <= y <= my + mheight/2):
                return False

        # If all tests are passed:
        return True

    # Calculates the first score of the marker using:
    #  - Aspect ration
    #  - Squareness
    #  - Solidity
    def getScore(self):
        # Get the values from minarearect
        (x,y), (width, height), angle = self.r

        # Calculate score from aspect ratio
        aspectRatio = min(width, height) / max(width, height)
        self.score += aspectRatio * 100

        # Calculate the area of the original contour
        area = cv2.contourArea(self.c)
        
        # Compute the solidity of the original contour
        # And add it to the score
        hullArea = cv2.contourArea(cv2.convexHull(self.c))
        solidity = area / float(hullArea)
        self.score += solidity * 100

        # Calculate the squareness of the contour
        # And add it to the score
        rarea = float(width * height)
        squareness = min(area,rarea) / max(area,rarea)
        self.score += squareness * 100

        return self.score

    # Calculate a secondary and more time intensive score 
    # This is currently only removing markers which also has the white border
    def getSecondaryScore(self, img, gray):
        # Get values from rect
        (x, y), (width, height), angle = self.r

        # Create a mask, which only contains the whole marker
        mask = np.uint8(np.ones(img.shape[:2]))
        mask = cv2.fillConvexPoly(mask, np.int0(cv2.boxPoints(self.r)), 255)

        # As a biproduct of this, it is quicker to calculate the average color now, than doing it later

        # Create a list of colors from the image
        # Which fit into the mask
        new = img[mask > 100]
        # Get average BGR value
        avgrgb = np.uint8([[np.average(new, axis=0)]])
        # Get average hue
        self.dhue = cv2.cvtColor(avgrgb, cv2.COLOR_BGR2HSV)[0, 0, 0] * 2

        # Create a rectangle, which will contain a marker, if the white border is present
        r2 = ((x,y), (width * 0.6, height * 0.6), angle)
        # And mask it out
        mask = cv2.fillConvexPoly(mask, np.int0(cv2.boxPoints(r2)), 1)
        
        # Caculate the average color of the border, same as before
        new = img[mask > 100]
        # Get average BGR values
        avgrgb = np.uint8([[np.average(new, axis=0)]])

        # However use saturation instead
        # Lower saturation = more chance of white border = lower score
        avgsat = cv2.cvtColor(avgrgb, cv2.COLOR_BGR2HSV)[0, 0, 1] * 2
        self.score += avgsat

        return self.score

    # Project the marker into a square on im
    def getProjMarker(self, im):
        # Get box points of min area rect
        k = cv2.boxPoints(self.r)

        # The corners of the marker
        pts = np.float32([k[3], k[0], k[2], k[1]])

        # Get transformation matrix and transform it on a n x n sqaure
        M = cv2.getPerspectiveTransform(pts, self.psqr)
        dst = cv2.warpPerspective(im, M, (self.msize + self.sco * 2, self.msize + self.sco * 2))
        dst = dst[self.sco:self.msize - self.sco,
                  self.sco:self.msize - self.sco]

        return dst

    # Draw the marker on img, with the score next to it
    def drawMarker(self, img, c, alphanum):
        # Draw rectangle around marker
        box = cv2.boxPoints(self.r) 
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (255,0,0), 2)

        # Get center of marker
        (x, y), _, _ = self.r

        # Draw score in the center
        cv2.putText(img, str(int(self.score)) + " " + c + " " + alphanum, (int(x), int(y)),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))

        # Return image with marker
        return img

    # Turn dhue into text
    def getColor(self):
        avghue = self.dhue

        # Return the color as text
        if (15 >= avghue or avghue >= 340): return "Red"
        elif (avghue <= 35): return "Orange"
        elif (avghue <= 70): return "Yellow"
        elif (avghue <= 140): return "Green"
        elif (avghue <= 200): return "Cyan"
        elif (avghue <= 255): return "Blue"
        elif (avghue <= 290): return "Purple"
        elif (avghue <= 315): return "Magenta"
        elif (avghue <= 340): return "Rose"
        return "Undefined"
