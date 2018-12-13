from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import math

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

def isBlack(array):
    if (array[0] < 50 and array[1] < 50 and array[2] < 50):
        return True


def take_picture():
    global camera
    global rawCapture
    rawCapture.truncate(0)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    return(image)

def crop_image_full_road(image):
    crop_start = 40
    crop_end = 125
    size_of_crop = crop_end-crop_start
    crop = image[crop_start:crop_end,0:640]
    return crop

def crop_image_for_stop(image):
    crop_start = 40
    crop_end = 125
    size_of_crop = crop_end-crop_start
    crop = image[crop_start:crop_end,200:400]
    return crop

## Return True if need to stop (red)
## Return False if green or black
def at_stop_sign(image):
    crop = crop_image_for_stop(image)
    seen_green = False
    for y in range(len(crop)):
        for x in range(len(crop[0])):
            if (isWhite(crop[y,x])):
                seen_green = True

    for y in range(len(crop)):
        for x in range(len(crop[0])):
            if (isRed(crop[y,x])):
                return True

    if (seen_green):
        return False
    else:
        return True
        
def find_yellow(crop):
    yellow = [-1,-1]
    for y in range(len(crop)-1,0,-2): #for every row
        for x in range(320,0,-10): # for every column
            if (isYellow(crop[y,x])):
                yellow = [y,x]
                return yellow
    if yellow == [-1,-1]:
        for y in range(len(crop)-1,0,-2): #for every row
            for x in range(320,640,10): # for every column
                if (isYellow(crop[y,x])):
                    yellow = [y,x]
                    return yellow
    else:
        return [-1,-1]

def find_white_from_yellow(crop, yellow):
    white = [-1,-1]
    line = yellow[0]
    for x in range(320,640):
        if (isWhite(crop[line,x])):
            white = [line,x]
            return white
    return white

## Call if don't find yellow
def find_white(crop):
    white = [-1,-1]
    for y in range(len(crop)-1,0,-2): #for every row
        for x in range(320,0,-10): # for every column
            if (isWhite(crop[y,x])):
                yellow = [y,x]
                return white
    if white == [-1,-1]:
        for y in range(len(crop)-1,0,-2): #for every row
            for x in range(320,640,10): # for every column
                if (isWhite(crop[y,x])):
                    white = [y,x]
                    return white
    else:
        return [-1,-1]

def find_midpoint(yellow,white):
    if (yellow[0] == -1):
        pass
    elif(white[0] == -1):
        pass
    else:
        pass