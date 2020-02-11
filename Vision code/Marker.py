import cv2
import numpy as np
from sklearn.cluster import KMeans

class Marker:
    ######################
    # External Variables #
    ######################
    # Marker ocr size
    msize = 40
    # Cutoff sides of projection
    sco = 5

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
    # Dominant color
    dcolor = None

    def __init__(self, c, approx):
        self.c = c
        self.approx = approx
        self.r = cv2.minAreaRect(approx)

    def getScore(self):
        # Get min area rectangle
        r = cv2.minAreaRect(self.approx)
        (x,y), (width, height), angle = r
        self.center = (int(x), int(y))

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

        # Calculate dominant color

        # Ignore smaller squares
        if (width < 25 or height < 25):
            self.score -= 1000

        #print(self.score, aspectRatio, solidity, squareness)
        return self.score

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

        # Invert colors for better OCR result
        return dst

    # Draw the marker on img, with the score next to it
    def drawMarker(self, img, c, alphanum):
        # Draw rectangle around marker
        box = cv2.boxPoints(self.r) 
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (255,0,0), 2)

        # Draw score
        cv2.putText(img, str(int(self.score)) + " " + c + " " + alphanum, self.center,
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))

        # Draw center
        cv2.circle(img, self.center, 1, (255,0,0))

        # Return image with marker
        return img

    def getColor(self, colorproj, ngproj):
        avghue = self.getDominantColor(colorproj)[0] * 2
        print(avghue)

        # Return the color as text
        if (30 >= avghue or avghue >= 330): return "Red"
        elif (avghue <= 30): return "Orange"
        elif (avghue <= 70): return "Yellow"
        elif (avghue <= 140): return "Yellow"
        elif (avghue <= 200): return "Light blue"
        elif (avghue <= 255): return "Blue"
        elif (avghue <= 290): return "Purple"
        elif (avghue <= 330): return "Pink"
        return "Undefined"

    def getDominantColor(self, img):
        reshape = img.reshape(
            (img.shape[0] * img.shape[1], 3))

        cluster = KMeans(n_clusters=2).fit(reshape)

        # Get the number of different clusters, create histogram, and normalize
        labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
        (hist, _) = np.histogram(cluster.labels_, bins=labels)
        hist = hist.astype("float")
        hist /= hist.sum()

        # Create frequency rect and iterate through each cluster's color and percentage
        colors = sorted([(percent, color) for (percent, color) in zip(hist, cluster.cluster_centers_)])
        
        print (cv2.cvtColor(
            np.uint8([[colors[1][1]]]), cv2.COLOR_BGR2HSV)[0, 0])

        # Return average as HSV
        return cv2.cvtColor(
            np.uint8([[colors[1][1]]]), cv2.COLOR_BGR2HSV)[0, 0]

    def visualize_colors(self, cluster, centroids):
        # Get the number of different clusters, create histogram, and normalize
        labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
        (hist, _) = np.histogram(cluster.labels_, bins=labels)
        hist = hist.astype("float")
        hist /= hist.sum()

        # Create frequency rect and iterate through each cluster's color and percentage
        rect = np.zeros((50, 300, 3), dtype=np.uint8)
        colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
        start = 0
        for (percent, color) in colors:
            print(color, "{:0.2f}%".format(percent * 100))
            end = start + (percent * 300)
            cv2.rectangle(rect, (int(start), 0), (int(end), 50),
                      color.astype("uint8").tolist(), -1)
            start = end
        return rect
