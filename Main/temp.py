from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import math
i = 0

camera = PiCamera()
rawCapture = PiRGBArray(camera)
rawCapture.truncate(0) 

def take_picture():
    global camera
    global rawCapture
    global i
    i = i+1
    rawCapture.truncate(0)
    camera.capture(rawCapture, format="bgr",use_video_port=True)
    image = rawCapture.array
    print(i)
    cv2.imwrite('full.jpg',image)
    return(image)

if __name__ == "__main__":

	take_picture()