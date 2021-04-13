#!/usr/bin/env python
import pytesseract
import cv2
from PIL import Image
import numpy as np
import matplotlib as plt
import imutils
import utils as ut


    	
cam = cv2.VideoCapture('file4.mp4')
# cam = cv2.VideoCapture(0)
# keep looping
while True:
	# grab the current frame and initialize the status text
	(grabbed, frame) = cam.read()
	frame = frame=cv2.resize(frame, (1080, 720), fx=0, fy=0, interpolation=cv2.INTER_NEAREST)
	
	# convert the frame to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (11, 11), 0) #7 7 def
	edged = cv2.Canny(blurred, 100, 200) # def 50 150
	# find contours in the edge map
	#cnts=cv2.findContours(edged.copy(),1,1)
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	
	# loop over the contours
	p = 0
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# print (peri)
		# ensure that the approximated contour is "roughly" rectangular
		if len(approx) >= 3 and len(approx) <= 5:
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
			#default was 25/25
			keepDims = w >100 and h > 100
			keepSolidity = solidity > 0.9
			keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2
			 
			# ensure that the contour passes all our tests
			
			if keepDims and keepSolidity and keepAspectRatio:
				# draw an outline around the target and update the status
				# text
				cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
				status = "Target(s) Acquired"
				

				w,h,arr=ut.transform(approx)
				pts2=np.float32([[0,0],[w,0],[0,h],[w,h]])
				pts1=np.float32(arr)
				M=cv2.getPerspectiveTransform(pts1,pts2)
				dst=cv2.warpPerspective(frame,M,(w,h))
				#image=cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
				# text=ut.ocr(image)
				# print("text",text)
				
				image_crop = cv2.resize(dst,(w,h),interpolation = cv2.INTER_NEAREST)
				cv2.imshow('OUTPUT',image_crop)
				

				# ut.image_rot(image_crop)


				#img_crop=ut.image_crop(approx,frame)
				
				#ut.proc(img_crop) 

				# compute the center of the contour region and draw the
				# crosshairs
				M = cv2.moments(approx)
				(cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
				# (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
				# (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
				#cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
				#cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)

			
	
	
	
					
	# # draw the status text on the frame
	# cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
	# 	(0, 0, 255), 2)
	# # show the frame and record if a key is pressed
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
cam.release()
cv2.destroyAllWindows()