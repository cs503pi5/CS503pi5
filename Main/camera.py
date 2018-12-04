import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
rawCapture = PiRGBArray(camera)
camera_midpoint = 320

def isYellow(array):
    if (array[0] < 200 and array[1] > 200 and array[2] > 200):
        return True

def isWhite(array):
    if (array[0] > 200 and array[1] > 200 and array[2] > 200):
        return True



yellow = [-1,-1]
white = [-1,-1]
for y in range(49,0,-1):
    for x in range(320,0,-1):
        if (isYellow(crop[y,x])):
            yellow = [y,x]
            break
line = yellow[0]
for x in range(320,640):
    if (isWhite(crop[line,x])):
        white = [line,x]
        break

#print(yellow)
#print(white)

midpoint = (white[1] + yellow[1])/2
#print(midpoint)

error = camera_midpoint - midpoint

print(error)
if (error > 0):
    print("turn right")
else:
    print("turn left")