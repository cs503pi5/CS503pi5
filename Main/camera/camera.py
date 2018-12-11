import serial
import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera

from pd_control import *
from drive_forward import*

# port = '/dev/ttyACM0'
# ser = serial.Serial(port, 115200)

## CAMERA STUFF
img_count = 0
camera = PiCamera()
rawCapture = PiRGBArray(camera)
rawCapture.truncate(0)
#640 width 480 height
camera_midpoint = 320
white_offset = 100
tolerance = 40
width = 350 #will change
prev_error = 0.0 

def isYellow(array):
    if (array[0] < 200 and array[1] > 200 and array[2] > 200):
        return True

def isWhite(array):
    if (array[0] > 200 and array[1] > 200 and array[2] > 200):
        return True

def isRed(array):
    if (array[0] < 150 and array[1] < 150 and array[2] > 200):
        return True

# def PD_error_camera(camera_error, camera_ref, K = 1, B = 0.01):
#     global prev_error
#     cam_ddot = -K*(camera_error - camera_ref) - B*(camera_error-prev_error)
#     prev_error = camera_error
#     return cam_ddot

def get_visual_error():
    global width
    global img_count
    red_seen = False
    a = (time.time())
    camera.capture(rawCapture, format="bgr")

#    print('capture image,',time.time()-a)

    image = rawCapture.array


    # 345-275 = 70
    img_count += 1

    cv2.imwrite('imgs/orig' + str(img_count) + '.jpg', image)
    crop = image[40:125,0:640]
    cv2.imwrite('imgs/crop' + str(img_count) + '.jpg', crop)

   # cv2.imwrite('orig.jpg', image)
   # crop = image[40:125,0:640]
   # cv2.imwrite('crop.jpg', crop)

    # init the yellow and white cord to -1,-1 
    yellow = [-1,-1]
    white = [-1,-1]

    # find the yellow pixel 
    for y in range(69,0,-10): #for every row
        for x in range(320,0,-10): # for every column
            if (isRed(crop[y,x])):
                red_seen = True
            if (isYellow(crop[y,x])):
                yellow = [y,x]
                break
#    print('after finding yellow', time.time()-a)
    # search for th white pixel in same row of yellow. theoretical should always find one
    line = yellow[0]
    for x in range(320,640):
        if (isWhite(crop[line,x])):
            white = [line,x]
            break
#    print('after find white', time.time()-a)
    midpoint = (white[1] + yellow[1])/2

    # if no yellow, pad white by width/2 to be the midponit 
    if (yellow[0] == -1 and yellow[1] == -1):
        midpoint = white[1] - (width/2)

    error = camera_midpoint - midpoint

    if (white[0] == -1 and white[1]== -1):
        midpoint = yellow[1] - (width/2)
    
    error = camera_midpoint - midpoint

    print('yellow: ' + str(yellow) + ", white: " + str(white) +  ', midpoint: '+ str(midpoint) + ', error: ' + str(error))


    # if (yellow[0] != -1):
    #     width = white[1] - yellow[1]

	# PD_error_camera(error, camera_ref = 0, K = 1, B = 0.1)
		
#    if (abs(error) > 100):
#        print("IGNORE, meaning camera found white in the left half  ")
#    else:
#        print(error)

    rawCapture.truncate(0)
#    print('right after truncate', time.time()-a)

    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    cv2.imwrite('VINCENT_NEITHER_PIC.jpg',image)
    return error


if __name__ == "__main__":
    i = 0
    while(1):
        error = get_visual_error()
        cam_ddot = PD_error_camera(error, 0, 0.05, 0.3)
        print("Visuals" ,str(error)+ ' , ' +str(cam_ddot))
        pwm_error = PD_to_PWM(cam_ddot)
        i = i+1
        if i > 5:
#            if (abs(pwm_error) < 40):
            run_straight_x_visual(pwm_error)
#            else:
#                run_straight()

