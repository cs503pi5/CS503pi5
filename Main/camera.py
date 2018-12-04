import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera


camera = PiCamera()
rawCapture = PiRGBArray(camera)
rawCapture.truncate(0)
camera_midpoint = 310
white_offset = 100
tolerance = 40

def isYellow(array):
    if (array[0] < 200 and array[1] > 200 and array[2] > 200):
        return True

def isWhite(array):
    if (array[0] > 200 and array[1] > 200 and array[2] > 200):
        return True


while(1):
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
#    cv2.imwrite('orig.jpg',image)
    crop = image[275:345,0:640]
#    cv2.imwrite('crop.jpg',crop)

    yellow = [-1,-1]
    white = [-1,-1]
    for y in range(69,0,-1):
        for x in range(320,0,-1):
            if (isYellow(crop[y,x])):
                yellow = [y,x]
                break
    line = yellow[0]
    for x in range(320,640):
        if (isWhite(crop[line,x])):
            white = [line,x]
            break
    
# print("yellow")
# print(yellow)
# print("white")
# print(white)

    midpoint = (white[1] + yellow[1])/2


    if (yellow[0] == -1 and yellow[1] == -1):
        midpoint = white[1] - white_offset

# print("midpoint")
# print(midpoint)
    error = camera_midpoint - midpoint

# print("error")
# print(error)
    if (error < tolerance and error > (-1*tolerance)):
        print("go straight")
    elif (error >= tolerance):
        print("turn right")
    else:
        print("turn left")
    rawCapture.truncate(0)