import matplotlib.pyplot as plt
import numpy as np
import cv2

area        = [0.36, 0.36, 0.64, 0.64, 0.68]
perimeter   = [0.36, 0.20, 0.40, 0.32, 0.33]

# plt.scatter(area, perimeter, color=['red','green','blue', 'yellow', 'orange'])
# plt.xlabel('Area')
# plt.ylabel('Perimeter')
# plt.show()



path = "Markers/Marker1.png"
dim = (500, 500)
img = cv2.imread(path)
img = cv2.resize(img, dim, interpolation= cv2.INTER_LINEAR)
cv2.imshow('image', img)



img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, img_bw) = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('gray', img_bw)



detector = cv2.SimpleBlobDetector_create()
keypoints = detector.detect(img_gray)
im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Keypoints", im_with_keypoints)




# img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)
# edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
# cv2.imshow('Edges', edges)


cv2.waitKey(0)