import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
rawCapture = PiRGBArray(camera)

def slope_contains(slopes, slope):
    for i in range(len(slopes)):
        if (slopes[i] - slope < .03 and slopes[i] - slope > -.03):
            return True
    return False

camera.capture(rawCapture, format="bgr")
image = rawCapture.array
cv2.imwrite('imgs/orig.jpg',image)
img = image[240:400,0:640]
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

rho = 1  
theta = np.pi / 180  
threshold = 15  
min_line_length = 50  
max_line_gap = 20  
line_image = np.copy(img) * 0  

lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                    min_line_length, max_line_gap)


slopes = []

true_lines = []

for i in range(len(lines[0])):
    arr = lines[0][i]
    m = float(arr[3] - arr[1]) / float(arr[2]-arr[0])
    if (not slope_contains(slopes,m)):
        slopes.append(m)
        true_lines.append(arr)
    

print(slopes)
for line in true_lines:
    x1,y1,x2,y2 = line[0],line[1],line[2],line[3]
    cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

cv2.imwrite('imgs/houghlines3.jpg',lines_edges)