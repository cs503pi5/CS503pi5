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
tolerance = 40
width = 350 # width of road; roughly 350-400 will change
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


# take picture
# crop image
# find yellow pixel; search left and the search right half
# if yellow is found, search for white on same line
#   if white is found good
#   else pad the yellow
# else that we dont see yellow, ensure we find white and padd from on that

def get_visual_error():
    global width
    global img_count
    red_seen = False
    a = (time.time())

    rawCapture.truncate(0)

    camera.capture(rawCapture, format="bgr")

#    print('capture image,',time.time()-a)

    image = rawCapture.array

    # 345-275 = 70
    img_count += 1
    crop_start = 40
    crop_end = 125
    size_of_crop = crop_end-crop_end
    # cv2.imwrite('imgs/orig' + str(img_count) + '.jpg', image)
    crop = image[crop_start:crop_end,0:640]
    # cv2.imwrite('imgs/crop' + str(img_count) + '.jpg', crop)

   # cv2.imwrite('orig.jpg', image)
   # crop = image[40:125,0:640]
   # cv2.imwrite('crop.jpg', crop)

    # init the yellow and white cord to -1,-1 
    yellow = [-1,-1]
    white = [-1,-1]
    midpoint = NULL
    # find the yellow pixel 
    def find_yellow():
        for y in range(size_of_crop-1,0,-2): #for every row
            for x in range(320,0,-10): # for every column
                if (isRed(crop[y,x])):
                    red_seen = True
                if (isYellow(crop[y,x])):
                    yellow = [y,x]
                    return yellow
        if yellow == [-1,-1]:
            for y in range(size_of_crop-1,0,-2): #for every row
                for x in range(320,640,10): # for every column
                    if (isRed(crop[y,x])):
                    red_seen = True
                 if (isYellow(crop[y,x])):
                    yellow = [y,x]
                    return yellow
        else:
            return [-1,-1]
    yellow = find_yellow    
    # print('after finding yellow', time.time()-a)
    # search for th white pixel in same row of yellow. theoretical should always find one

    # if yellow is found, find the white line in the right half
    if yellow != [-1,-1]:
        line = yellow[0]
        for x in range(320,640):
            if (isWhite(crop[line,x])):
                white = [line,x]
                break
        # if white is found we gucci
        if white != [-1,-1]:
            midpoint = (white[1] + yellow[1])/2
            error = camera_midpoint - midpoint
            return error
        # white not found, pad yellow
        else:
            midpoint = yellow[1] + (width/2)
            error = camera_midpoint - midpoint
            return error
#    print('after find white', time.time()-a)
    # no yellow found, find white from the top of the crop on the right side. should only ever be on the right side
    else:
        for y in range(size_of_crop-1,0,-2): #for every row
            for x in range(320,640,10): # for every column
                if (isWhite(crop[y,x])):
                    white = [y,x]
                    midpoint = white[1] - (width/2)
                    error = camera_midpoint - midpoint
                    return error
    
    print('yellow: ' + str(yellow) + ", white: " + str(white) +  ', midpoint: '+ str(midpoint) + ', error: ' + str(error))


    rawCapture.truncate(0)

    
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

