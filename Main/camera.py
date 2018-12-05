import serial
import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera

# port = '/dev/ttyACM0'
# ser = serial.Serial(port, 115200)

camera = PiCamera()
rawCapture = PiRGBArray(camera)
rawCapture.truncate(0)
camera_midpoint = 310
white_offset = 100
tolerance = 40
width = 400 #will change
prev_error = 0

def isYellow(array):
    if (array[0] < 200 and array[1] > 200 and array[2] > 200):
        return True

def isWhite(array):
    if (array[0] > 200 and array[1] > 200 and array[2] > 200):
        return True

def isRed(array):
    if (array[0] < 150 and array[1] < 150 and array[2] > 200):
        return True

def PD_error_camera(camera_error, camera_ref, K = 1, B = 0.01):
    global prev_error
    cam_ddot = -K*(camera_error - camera_ref) - B*(camera_error-prev_error)
    prev_error = camera_error
    return cam_ddot  

def get_error():
    global width
    red_seen = False
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    crop = image[275:345,0:640]

    yellow = [-1,-1]
    white = [-1,-1]
    for y in range(69,0,-1):
        for x in range(320,0,-1):
            if (isRed(crop[y,x])):
                red_seen = True
            if (isYellow(crop[y,x])):
                yellow = [y,x]
                break
    line = yellow[0]
    for x in range(320,640):
        if (isWhite(crop[line,x])):
            white = [line,x]
            break
      
    midpoint = (white[1] + yellow[1])/2


    if (yellow[0] == -1 and yellow[1] == -1):
        midpoint = white[1] - (width/2)

    error = camera_midpoint - midpoint

    if (yellow[0] != -1):
        width = white[1] - yellow[1]

    print(error)

    rawCapture.truncate(0)

    return error

if __name__ == "__main__":
    while(1):
        get_error()