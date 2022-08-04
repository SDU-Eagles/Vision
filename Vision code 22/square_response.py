import cv2
import numpy as np

def square_response(img, debug=False):

    
    src = cv2.GaussianBlur(img, (3, 3), 0)
    
    # Only use 'A' channel
    temp = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
    img_lab = temp[:, :, 1]

    # Get gradients and their direction with Sobel
    scale = 3
    delta = 0
    ddepth = cv2.CV_16S
    grad_x = cv2.Sobel(img_lab, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(img_lab, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)

    # Complex number response
    edge_directions = grad_x + grad_y*(1j)  # Complex number representation
    v1 = edge_directions ** 2
    v2 = v1 ** 2
    temp1 = np.real(v1) / np.max(np.abs(v1)) + 0.5
    temp2 = np.real(v2) / np.max(np.abs(v2)) + 0.5
    temp1 = np.real(v1) / np.max(np.abs(v1)) 
    temp2 = np.real(v2) / np.max(np.abs(v2))

    kernel = np.ones((110, 110), np.float32)/110/110
    v2_real = cv2.filter2D(np.real(v2), -1, kernel)
    v2_imag = cv2.filter2D(np.imag(v2), -1, kernel)
    v3 = v2_real + v2_imag*(1j)


    # Square response
    response = np.abs(v3) / np.max(np.abs(v3))
    # response = np.abs(v3) / np.max(np.abs(v3)) + 0.5
    
    response_weight = 100
    

    if debug:
        cv2.imwrite("output/01_orig.png", img)
        cv2.imwrite("output/02_a-channel.png", img_lab)
        cv2.imwrite("output/02_v1.png", temp1 * 127)
        cv2.imwrite("output/03_v2.png", temp2 * 127)
        cv2.imwrite("output/05_strength.png", response * response_weight)
        
        
    return response * response_weight




if __name__ == "__main__":
    
    filename = "Sample_images/9.jpg"
    img = cv2.imread(filename)
    
    response = square_response(img, debug=False)
    
    cv2.imwrite("output/square_response.png", response)
    
    print(np.median(response))
    