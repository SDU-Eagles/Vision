#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  folder_resize.py
#  
#  Copyright 2019 thanasis <thanasis@thanasis>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import cv2
import numpy as np
import matplotlib.pyplot as plt
import  glob
import  sys
from scipy.misc import imresize

filenames = glob.glob("/home/thanasis/Documents/eagles/Markers-eagles -20190213T183437Z-001/Markers-eagles /*.jpg")
filenames.sort()
images = [cv2.imread(img) for img in filenames]
d=0
for img in images:
	imS = cv2.resize(img, (640, 480)) 
	cv2.imshow("edges", imS)
	#print (img)
	filename = "/home/thanasis/Documents/eagles/Markers-eagles -20190213T183437Z-001/resized/resized_%d.jpg"%d
	cv2.imwrite(filename, imS)
	d+=1
	cv2.waitKey(0)
	cv2.destroyAllWindows()
