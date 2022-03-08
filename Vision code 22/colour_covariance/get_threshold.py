import cv2 
import numpy as np   

path = "5.jpg"
img = cv2.imread(path)
pixels = np.reshape(img, (-1, 3))

img_annotated = cv2.imread('5-annotated.jpg')
mask = cv2.inRange(img_annotated, (0, 0, 245), (10, 10, 256))

# Cause Illustartor exported it weird, and I ain't fixing it x)
height, width, channels = img.shape 
mask = cv2.resize(mask, (width, height), interpolation= cv2.INTER_LINEAR)
# Back to the regular scheduled program...

mask_pixels = np.reshape(mask, (-1))

cov = np.cov(pixels.transpose(), aweights=mask_pixels)
cov_inv = np.linalg.inv(cov)
avg = np.average(pixels.transpose(), weights=mask_pixels, axis=1)
print(cov_inv)
print()
print(avg)


# Mahalanobis based segmentation
shape = pixels.shape
diff = pixels - np.repeat([avg], shape[0], axis=0)

mahalanobis_dist = np.sum(diff * (diff @ cov_inv), axis=1)
mahalanobis_distance_image = np.reshape(mahalanobis_dist, (img.shape[0], img.shape[1]))
mahal_scaled_dist_image = 255 * mahalanobis_distance_image / np.max(mahalanobis_distance_image)

_, mahalanobis_segmented = cv2.threshold(mahalanobis_distance_image, 40, 255, cv2.THRESH_BINARY_INV)
mahalanobis_segmented = mahalanobis_segmented.astype(np.uint8)
cv2.imwrite("5-mahalanobis_dist_segmented.jpg", mahalanobis_segmented)