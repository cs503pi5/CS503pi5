import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera

def euc_distance(array):
    sum = 0
    for i in array:
        sum = sum + (i**2)
    return math.sqrt(sum)

def white_color(array):
    threshold = 190
    if (array[0] > threshold and array[1] > threshold and array[2] > threshold):
        return True
    return False

def line_coords(image, coords):
    h = image.shape[0]
    print(h)
    w = image.shape[1]
    print(w)
    for y in range(0, h):
        first = False
        for x in range(0, w):
            GBR = image[y, x]
            if (white_color(GBR) and first == False):
                coords.append(x)
                coords.append(y)
                first = True


camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

while (True):
	white_line = []
	camera.capture(rawCapture, format="bgr")
	image = rawCapture.array
	cv2.imwrite("orig.jpg", image)
	crop_img = image[420:440, 50:500]
	cv2.imwrite("crop.jpg", crop_img)
	line_coords(crop_img, white_line)
	if (len(white_line) > 2):
		x0, y0, x1, y1 = white_line[0], white_line[1], white_line[len(white_line)-2], white_line[len(white_line)-1]
		m = 0
		if (float(x1-x0)!= 0):
			m = float(y1-y0)/float(x1-x0)
		b = y1 - (m * x1)
		print ("Slope: {} \nY-Intercept: {}".format(m,b)) 
		rawCapture.truncate(0)
	else:
		print("no line...")
		rawCapture.truncate(0)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()



##img = cv2.imread("3.jpg")
##crop_img = img[400:440, 50:500]
##cv2.imwrite("crop.jpg", crop_img)

