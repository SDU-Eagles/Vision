import cv2
import pytesseract
import numpy as np
#https://github.com/spmallick/learnopencv/blob/master/BlobDetector/blob.py
from PIL import Image
from matplotlib import pyplot as plt
import multiprocessing as mp
# g e a r g e...

# def f(x):
#     while 1:
#         pass  # infinite loop

# import multiprocessing as mp
# n_cores = mp.cpu_count()
# with mp.Pool(n_cores) as p:
#     p.map(f, range(n_cores))

def image_rot(img):
    rows,cols=img.shape
    i=0
    angle=0
    for angle in range (0,360,90):
        M=cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
        dst = cv2.warpAffine(img,M,(cols,rows))
        text=detect_test(dst)
        if (text == "G") :
            exit()
        cv2.imshow("rot",dst)
        print("text",text)
        #print("angle",angle)

    

def save_to_file(img):
    d+=1
    filename="/home/kiagkons/Documents/Eagles/Sdu_Eagles_Electronics/Detection/letters/im_%d.jpg"%d
    cv2.imwrite(filename,sharpened)
    print("done",d)

def detect_test(img):
    config = ('-l eng --oem 1 --psm 3')
    text = pytesseract.image_to_string(img, config=config)
    return text


width=1920
height=1080
cap = cv2.VideoCapture('samplevideo.mp4')
p=0
print("1")
# while True :
while cap.isOpened():
    ret, frame = cap.read()
    frame=cv2.resize(frame, (width, height), fx=0, fy=0, interpolation=cv2.INTER_NEAREST)
    #frame=cv2.resize(frame,(width,height))
    #image=frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    cv2.imshow('frame',frame)
    #img= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    p=p+1
    print('frame no.',p)


    # Simple blob detector
    params = cv2.SimpleBlobDetector_Params()

    # set threshold
    #for 640*480 min 10 max 200
    params.minThreshold = 10
    params.maxThreshold = 200

    # Area filtering
    #640*480 75,250
    params.filterByArea = True
    params.minArea = 75
    params.maxArea = 250


    params.filterByCircularity = True
    params.minCircularity = 0.75

    params.filterByConvexity = True
    params.filterByInertia = False
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(frame)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
    # the size of the circle corresponds to the size of blob

    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (125,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    #print("test", keypoints)
    # Show blobs

    cv2.imshow("Keypoints", im_with_keypoints)
    print("frame no.=",p)
    key = cv2.waitKey(25) & 0xFF
    if key == ord("q"):
        break
    d=0
    for k in keypoints:
        d+=1

        (x,y) = k.pt
        x = int(round(x))
        y = int(round(y))
        s=k.size
        s=int(round(s))
        a=int(round(x+(s/2))+4)
        b=int(round(y+(s/2))+4)
        c = int(round(x - (s / 2))-2)
        d = int(round(y - (s / 2))-2)
        #rect1=x+4-s
        #rect2=y+4-s
        #rect3=int(round(2*s-8))
        #rect4=int(round(2*s-8))
        cv2.rectangle(frame,(a,b), (c,d), (0,0,0),3)
        #cv2.imshow("with frame", frame)
        #Mat cropedImage = fullImage(Rect(X,Y,Width,Height));
        #crop_img=cv2.copyMakeBorder(frame,a,d,c,b, cv2.BORDER_REPLICATE)
        crop_img = frame[int(y-6):int(y+6),int(x-6):int(x+6)]
        crop_img = cv2.resize(crop_img, (30,30))
        cv2.imshow("crop_img", crop_img)
        # sharpening
        kernel = np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]])
        img = cv2.filter2D(crop_img, -1, kernel)        
        
        # # img blur
        # img = cv2.GaussianBlur(img,(5,5),0)
        # img=cv2.addWeighted(img,1.5,img,-0.5,0)
        
        #ret,bina = cv2.threshold(img,180,255,cv2.THRESH_BINARY_INV)        
        #th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,9,1)
        #kern = np.ones((3,3),np.uint8)
        # th3 = cv2.erode(th3,kern,iterations = 1)
        #th3 = cv2.dilate(th3,kern,iterations = 1)
        # th3 = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kern)

        #cv2.imshow("binary", bina)
        cv2.imshow("sharp", img)
        #cv2.imshow("adaptive",th3)
        
        image_rot(icrop)

        # text = pytesseract.image_to_string(crop_img)
        # #os.remove(filename)
        # print("Text detected",text)

        # show the output images
        

cap.release()
cv2.destroyAllWindows()


