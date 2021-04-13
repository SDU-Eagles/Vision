import tesserocr
from tesserocr import PyTessBaseAPI
from PIL import Image
import pytesseract
import cv2
import threading
import numpy as np

# Run OCR on 'img' with an initialized tesserocr 'api'
def OCR(im,api):
    # Dilate to remove noise and help the OCR algorithm
    kernel = np.ones((2, 2), np.uint8)
    im = cv2.dilate(im, kernel, iterations=1)

    # Invert colors for better result
    # This makes sure the letter is black on white
    im = cv2.bitwise_not(im)

    # Show OCR image for debug purposes
    #cv2.imshow("OCR", im)

    # The highest word confidence
    conf = 0
    # The character with the highest word confidence
    char = ''

    # Run OCR on all 4 rotations of the image
    for i in range(0, 4):
        # Convert image to PIL and send it to Tesseract
        api.SetImage(Image.fromarray(im))

        # TODO Sort out non-alphanumeric characters
        # And make this check afterwards
        # TODO Change it find only one character
        
        # Make sure it has only found one text
        if len(api.AllWordConfidences()) == 1:
            # Check if the character is higher than the highest score
            if api.AllWordConfidences()[0] > conf:
                # If it is, then change the highscore
                conf = api.AllWordConfidences()[0]
                char = api.GetUTF8Text().strip()
        # Rotate the image 90 degrees
        im = cv2.rotate(im, cv2.ROTATE_90_CLOCKWISE)
        
    # Print the highscore, with the confidence
    #print("Character: {0} : Confidence {1}".format(char,conf))
    return char
