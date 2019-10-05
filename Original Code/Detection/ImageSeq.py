import cv2
import os


from skimage.io import imread_collection

#your path
col_dir = '/Documents/Eagles/Sdu_Eagles_Electronics/Markers-eagles/*.jpg'

#creating a collection with the available images
col = imread_collection(col_dir)

