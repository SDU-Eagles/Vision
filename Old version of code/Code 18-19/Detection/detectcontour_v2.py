#!/usr/bin/env python
import pytesseract
import cv2
from PIL import Image
import numpy as np
import matplotlib as plt
import imutils


def image_crop(c, frame):
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)

    ext_left = tuple(c[c[:, :, 0].argmin()][0])
    ext_right = tuple(c[c[:, :, 0].argmax()][0])
    ext_top = tuple(c[c[:, :, 1].argmin()][0])
    ext_bot = tuple(c[c[:, :, 1].argmax()][0])

    # roi_corners = np.array([box], dtype=np.int32)

    # cv2.polylines(frame, roi_corners, 1, (255, 0, 0), 3)
    cropped_image = frame[ext_top[1]:ext_bot[1], ext_left[0]:ext_right[0]]
    cv2.imshow('image', cropped_image)
    return cropped_image


def image_rot(img):
    rows, cols = img.shape
    i = 0
    angle = 0
    for angle in range(0, 360, 90):
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        dst = cv2.warpAffine(img, M, (cols, rows))
        text = ocr(dst)
        cv2.imshow("rot", dst)
        print("text", text)
    # print("angle",angle)


def save_to_file(img):
    d += 1
    filename = "/home/kiagkons/Documents/Eagles/Sdu_Eagles_Electronics/Detection/letters/im_%d.jpg" % d
    cv2.imwrite(filename, img)
    print("done", d)


def proc(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.GaussianBlur(img, (3, 3), 0)

    ret, bina = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 1)
    kern = np.ones((5, 5), np.uint8)
    th3 = cv2.erode(th3, kern, iterations=1)
    # th3 = cv2.dilate(th3,kern,iterations = 1)
    # th3 = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kern)
    text1=ocr(bina)
    # text2=ocr(th3)
    # image_rot(bina)
    print("binia",text1)
    # print("adaptive",text2)

    cv2.imshow("binary_output", bina)


# cv2.imshow("sharp", img)
# cv2.imshow("adaptive",th3)


def ocr(img):
    config = ('-l eng --oem 1 --psm 10')
   # text = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 10')
    text = pytesseract.image_to_string(img, config=config)
    return text


cam = cv2.VideoCapture('file4.mp4')
# cam = cv2.VideoCapture(0)
# keep looping
while True:
    # grab the current frame and initialize the status text
    (grabbed, frame) = cam.read()
    frame = frame = cv2.resize(frame, (1080, 720), fx=0, fy=0, interpolation=cv2.INTER_NEAREST)
    status = "No Targets"
    # cv2.imshow("original", frame)
    # convert the frame to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)
    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    p = 0
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
                # draw an outline around the target and update the status
                # text
                cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                print('contour', approx)
                status = "Target(s) Acquired"

                # compute the center of the contour region and draw the
                # crosshairs
                M = cv2.moments(approx)
                (cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
                # (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                # (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                # cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
                # cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)
                img_crop = image_crop(approx, frame)
                proc(img_crop)
    # # draw the status text on the frame
    # cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    # 	(0, 0, 255), 2)
    # # show the frame and record if a key is pressed
    cv2.imshow("Detected", frame)
    key = cv2.waitKey(50) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
cam.release()
cv2.destroyAllWindows()