import cv2
import numpy as np

def main():
    # filename = "input/Screenshot from 2022-05-06 10-18-03.png"
    # filename = "input/smple_images/6.jpg"
    # filename = "input/smple_images/5.jpg"
    # filename = "input/smple_images/2.jpg"
    filename = "Sample_images/1.jpg"
    img = cv2.imread(filename)
    cv2.imwrite("output/01_orig.png", img)

    scale = 3
    delta = 0
    ddepth = cv2.CV_16S

    src = cv2.GaussianBlur(img, (3, 3), 0)
    
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # Only use green color channel
    #gray = src[:, :, 1]
    temp = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
    gray = temp[:, :, 1]
    cv2.imwrite("output/02_grayscale.png", gray)


    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale,
delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale,
delta=delta, borderType=cv2.BORDER_DEFAULT)

    edge_directions = 1.0*grad_x + 1.0*grad_y*(1j)
    v1 = edge_directions * edge_directions
    v2 = v1 * v1
    temp1 = np.real(v1) / np.max(np.abs(v1)) + 0.5
    temp2 = np.real(v2) / np.max(np.abs(v2)) + 0.5
    #cv2.imshow("v1", temp1 * 127)
    #cv2.imshow("v2", temp2 * 127)
    cv2.imwrite("output/02_v1.png", temp1 * 127)
    cv2.imwrite("output/03_v2.png", temp2 * 127)


    kernel = np.ones((110, 110),np.float32)/110/110
    v2_real = cv2.filter2D(np.real(v2), -1, kernel)
    v2_imag = cv2.filter2D(np.imag(v2), -1, kernel)
    v3 = v2_real + v2_imag * 1j

    temp3 = np.abs(v3) / np.max(np.abs(v3)) + 0.5
    #cv2.imshow("v3", temp3 * 100)
    cv2.imwrite("output/05_strength.png", temp3 * 100)


    #cv2.waitKey(-1)
    
    pass


main()
