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
fixed_width = 200
prev_error = 0.0 



def isYellow(array):
    if (array[0] < 200 and array[1] > 200 and array[2] > 200):
        return True

def isWhite(array):
    if (array[0] > 200 and array[1] > 200 and array[2] > 200):
	    return True

def isRed(array):
    if (array[0] < 130 and array[1] < 130 and array[2] > 190):
	    return True

def isBlack(array):
    if (array[0] < 50 and array[1] < 50 and array[2] < 50):      
	    return True

i = 0
def take_picture():
    global camera
    global rawCapture
    global i
    i = i+1
    rawCapture.truncate(0)
    camera.capture(rawCapture, format="bgr",use_video_port=True)
    image = rawCapture.array
    print(i)
    #cv2.imwrite('full.jpg',image)
    return(image)

def crop_image_full_road(image):
    crop_start = 40
    crop_end = 125
    size_of_crop = crop_end-crop_start
    crop = image[crop_start:crop_end,0:640]
    return crop

def crop_image_for_stop(image):
    #240:320,150:400
    crop_start = 50
    crop_end = 130
    size_of_crop = crop_end-crop_start
    crop = image[crop_start:crop_end,150:400]
    return crop

## Return True if need to stop (red)
## Return False if green or black
def at_stop_sign(crop):
    seen_green = False
    seen_red = False
    for y in range(len(crop)):
        for x in range(len(crop[0])):
            if (isWhite(crop[y,x])):
                seen_green = True
    for y in range(len(crop)):
        for x in range(len(crop[0])):
            if (isRed(crop[y,x])):
                seen_red = True
    if (seen_green):
        return False
    else:
        return seen_red
        
def find_yellow(crop):
    yellow = [-1,-1]
    for y in range(len(crop)-1,0,-2): #for every row
        for x in range(320,0,-10): # for every column
            if (isYellow(crop[y,x])):
                yellow = [y,x]
                print("yellow",yellow)
                return yellow
    if yellow == [-1,-1]:
        for y in range(len(crop)-1,0,-2): #for every row
            for x in range(320,640,10): # for every column
                if (isYellow(crop[y,x])):
                    yellow = [y,x]
                    print("yellow",yellow)
                    return yellow
    return [-1,-1]

def find_white_from_yellow(crop, yellow):
    white = [-1,-1]
    line = yellow[0]
    for x in range(320,640):
        if (isWhite(crop[line,x])):
            white = [line,x]
            print("white", white)
            return white
    return white

## Call if don't find yellow
def find_white(crop):
    white = [-1,-1]
    for y in range(len(crop)-1,0,-2): #for every row
        for x in range(320,0,-10): # for every column
            if (isWhite(crop[y,x])):
                print("white",white)
                white = [y,x]
                return white
    if white == [-1,-1]:
        for y in range(len(crop)-1,0,-2): #for every row
            for x in range(320,640,10): # for every column
                if (isWhite(crop[y,x])):
                    print("white",white)
                    white = [y,x]
                    return white
    return [-1,-1]

def find_midpoint(crop):
    fixed_width_white = 150
    fixed_width_yellow = 130
    yellow = find_yellow(crop)

    if (yellow[0] != -1):
        white = find_white_from_yellow(crop,yellow)
        if (white[0] != -1):
            if (yellow[1]<white[1]):
                print("case 1")
                midpoint = (white[1] + yellow[1])/2
                print(midpoint)
                return midpoint
            else:
                white = find_white(crop)
                print("case 3")
                midpoint = (white[1] - fixed_width_white)
                print(midpoint)
                return midpoint
        else:
            print("case 2")
            midpoint = (yellow[1] + fixed_width_yellow)
            print(midpoint)
            return midpoint

    else:
        white = find_white(crop)
        if (white[0] != -1):
            print("case 3")
            midpoint = (white[1] - fixed_width_white)
            print(midpoint)
            return midpoint
        else:
            midpoint = 320
            print("case 4")
            print(midpoint)
            return midpoint


def calculate_error(midpoint):
    return (camera_midpoint - midpoint)

def PD_error_camera(camera_error, camera_ref, K, B):
    global prev_error
    cam_ddot = -K*(camera_error - camera_ref) - B*(camera_error-prev_error)
    prev_error = camera_error
    return cam_ddot



if __name__ == "__main__":
    # #Yellow = []
    # image = take_picture()
    # crop = crop_image_for_stop(image)
    # flag = at_stop_sign(crop)
    # if (not flag): #green light
    #     #continue
    #     cropFull = crop_image_full_road(image)
	# mid = find_midpoint(cropFull)
	# err = calculate_error(mid)
	# PD_error_camera(err, camera_ref = 0, K = 0.015, B = 0.01)
	# #Yellow = find_yellow(cropFull)
	# #if (Yellow[0]!=-1):
	# #    find_white_from_yellow(cropFull, isYellow)
	# #else:
	# #    find_white(cropFull)
    # else: #red light
    #     pass
	# #stop the car
    take_picture()
