import cv2
import numpy as np

def square_response(img, marker_image_size, debug=False):

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
    temp1 = np.real(v1) / np.max(np.abs(v1)) + 0.5  # Show gradients on grey bg
    temp2 = np.real(v2) / np.max(np.abs(v2)) + 0.5  

    kernel = np.ones((int(marker_image_size/2), int(marker_image_size/2)), np.float32)
    v2_real = cv2.filter2D(np.real(v2), -1, kernel)
    v2_imag = cv2.filter2D(np.imag(v2), -1, kernel)
    gradient_vectors = v2_real + v2_imag*(1j)


    # Angle of complex numbers
    angles = cv2.phase(v2_real, v2_imag) / 4    # Go from 0:2pi to 0:pi/2
    angles = np.transpose(angles)
    


    # Square response (normalised to 0-100)
    response = 100 * np.abs(gradient_vectors) / np.max(np.abs(gradient_vectors))
    

    if debug:
        cv2.imwrite("output/01_orig.png", img)
        cv2.imwrite("output/02_a-channel.png", img_lab)
        cv2.imwrite("output/02_v1.png", temp1 * 127)
        cv2.imwrite("output/03_v2.png", temp2 * 127)
        cv2.imwrite("output/05_strength.png", response)
        
        mag = cv2.magnitude(v2_real, v2_imag)
        orien = cv2.phase(v2_real, v2_imag, angleInDegrees=True)
        orien = orien / 2. # Go from 0:360 to 0:180 
        hsv = np.zeros_like(img)
        # hsv[..., 0] = orien # H (in OpenCV between 0:180)
        hsv[..., 0] = np.rad2deg(np.transpose(angles)) # H (in OpenCV between 0:90)
        hsv[..., 1] = 255 # S
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX) # V 0:255

        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imwrite("output/06_gradient_direction.png", bgr)
        
        print("Wrote images to path: 'output/0X_attribute.png'")
        
        
    return response, angles





if __name__ == "__main__":
    
    filename = "Sample_images/9.jpg"
    img = cv2.imread(filename)
    
    response, angles = square_response(img, 250, debug=True)
    
    cv2.imwrite("output/square_response.png", response)
    

