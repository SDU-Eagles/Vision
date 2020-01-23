import cv2

class Marker:
    # Center of the marker
    # Not in use
    center = (0,0)

    # The registered score of the marker
    score = 0

    # The original contour defining the marker
    c = None

    # An approximate poly describing c
    approx = None
    

    def __init__(self, c, approx):
        self.c = c
        self.approx = approx

    def getScore(self):
        # Get min area rectangle
        r = cv2.minAreaRect(self.approx)
        (x, y), (width, height), angle = r

        # Calculate aspect ratio
        aspectRatio = min(width, height) / max(width, height)

        # Compute the solidity of the original contour
        # TODO Change this to use convex hull and min area rect
        area = cv2.contourArea(self.c)
        hullArea = cv2.contourArea(cv2.convexHull(self.c))
        solidity = area / float(hullArea)

        # Calculate and return the score
        return aspectRatio * 100 + solidity * 100
