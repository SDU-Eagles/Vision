import pytesseract
import cv2
from PIL import Image
import numpy as np
import matplotlib as plt
import imutils

#all usefull functioned are included here!
#saved my ass // tesseract 3.05 installation from https://www.lucacerone.net/2017/installing-tesseract-3-0-5-on-ubuntu-16-04/

def transform(pos):
    # This function is used to find the corners of the object and the dimensions of the object
    
    pts=[]
    n=len(pos)
    for i in range(n):
        pts.append(list(pos[i][0]))
       
    sums={}
    diffs={}
    tl=tr=bl=br=0
    for i in pts:
        x=i[0]
        y=i[1]
        sum=x+y
        diff=y-x
        sums[sum]=i
        diffs[diff]=i
    sums=sorted(sums.items())
    diffs=sorted(diffs.items())
    n=len(sums)
    rect=[sums[0][1],diffs[0][1],diffs[n-1][1],sums[n-1][1]]
    #      top-left   top-right   bottom-left   bottom-right
   
    h1=np.sqrt((rect[0][0]-rect[2][0])**2 + (rect[0][1]-rect[2][1])**2)     #height of left side
    h2=np.sqrt((rect[1][0]-rect[3][0])**2 + (rect[1][1]-rect[3][1])**2)     #height of right side
    h=max(h1,h2)
   
    w1=np.sqrt((rect[0][0]-rect[1][0])**2 + (rect[0][1]-rect[1][1])**2)     #width of upper side
    w2=np.sqrt((rect[2][0]-rect[3][0])**2 + (rect[2][1]-rect[3][1])**2)     #width of lower side
    w=max(w1,w2)
   
    return int(w),int(h),rect



def image_crop(c,frame):
    
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
			#cv2.imshow("rot", dst)
			("text", text)
			# print("angle",angle)


def save_to_file(img):
    d+=1
    filename="/home/kiagkons/Documents/Eagles/Sdu_Eagles_Electronics/Detection/letters/im_%d.jpg"%d
    cv2.imwrite(filename,img)
    print("done",d)

def proc(img):
    
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.GaussianBlur(img,(3,3),0)
    ret,bina = cv2.threshold(img,180,255,cv2.THRESH_BINARY_INV)        
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,9,1)
    kern = np.ones((5,5),np.uint8)
    th3 = cv2.erode(th3,kern,iterations = 1)
    # th3 = cv2.dilate(th3,kern,iterations = 1)
    # th3 = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kern)
   
    text1=ocr(bina)
    text2=ocr(th3)
    #image_rot(bina)
    print("binia",text1)
    print("adaptive",text2)


    cv2.imshow("binary", bina)
    # cv2.imshow("sharp", img)
    # cv2.imshow("adaptive",th3)
		


def ocr(img):    	
    #config = ('-l eng --oem 1 --psm 10')
    text =pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 10')
    #text = pytesseract.image_to_string(img, config=config)	
    return text

