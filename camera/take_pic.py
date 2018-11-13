from picamera import PiCamera
from time import sleep
import datetime
import cv2

#Initialize object
camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture('/home/gandalf_student/CS503pi5/camera/pics/road.jpg')
camera.stop_preview()

img = cv2.imread("pics/road.jpg")
crop_img = img[380:440, 20:640]
cv2.imwrite("pics/crop.jpg", crop_img) 