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
    if (euc_distance(array) > 300):
        return True
    return False

def yellow_color(array):
    if (euc_distance(array) > 200 and euc_distance(array) < 300):
        return True
    return False

def line_coords(image, coords):
    h = image.shape[0]
    w = image.shape[1]

    for y in range(0, h):
        first = False
        for x in range(w/2, w):
            GBR = image[y, x]
            if (white_color(GBR) and first == False):
                coords.append(x)
                coords.append(y)
                first = True


def yellow_coords(image, coords):
    h = image.shape[0]
    w = image.shape[1]/2

    for y in range(0, h):
        first = False
        for x in range(w, 0, -1):
            GBR = image[y, x]
            if (yellow_color(GBR) and first == False):
                coords.append(x)
                coords.append(y)
                first = True

def print_img(image):
    h = image.shape[0]
    w = image.shape[1]

    for y in range(0, h):
        for x in range(0, w):
            GBR = image[y, x]
            print(GBR),
        print("\n")

def print_euc(image):
    h = image.shape[0]
    w = image.shape[1]

    for y in range(0, h):
        for x in range(0, w):
            GBR = image[y, x]
            print(euc_distance(GBR)),
        print("\n")

def main():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 64
    rawCapture = PiRGBArray(camera, size=(640, 480))

    wx0, wy0, wx1, wy1, wm, wb = 0,0,0,0,0,0
    yx0, yy0, yx1, yy1, ym, yb = 0,0,0,0,0,0

    i = 0
    for frame in camera.capture_continuous(rawCapture, format="bgr"):
        white_line = []
        yellow_line = []

        crop_img = frame.array[380:440, 20:640]

        line_coords(crop_img, white_line)
        yellow_coords(crop_img, yellow_line)

        print(i)
        if (len(white_line) > 2):
            wx0, wy0, wx1, wy1 = white_line[0], white_line[1], white_line[len(white_line)-2], white_line[len(white_line)-1]
            wm = float((-wy1)-wy0)/float(wx1-wx0)
            wb = wy1 - (wm * wx1)
            print ("White:\nSlope: {} \nY-Intercept: {}".format(wm,wb)) 
            rawCapture.truncate(0)
        else:
            print("no white line...")
            rawCapture.truncate(0)

        if (len(yellow_line) > 2):
            yx0, yy0, yx1, yy1 = yellow_line[0], yellow_line[1], yellow_line[len(yellow_line)-2], yellow_line[len(yellow_line)-1] 
            ym = float((-yy1)-yy0)/float(yx1-yx0)
            yb = yy1 - (ym * yx1)
            print ("Yellow:\nSlope: {} \nY-Intercept: {}".format(ym,yb)) 
            rawCapture.truncate(0)
        else:
            print("no yellow line ...")
            rawCapture.truncate(0)

        midpoint = (wx0 + yx0)/2
        print ("Midpoint: {} \nDistance from left: {}".format(midpoint, midpoint-yx0))
        i = i+1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   

if __name__ == "__main__":
    main()