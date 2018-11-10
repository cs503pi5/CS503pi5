from picamera import PiCamera
from time import sleep
import datetime

#Initialize object
camera = PiCamera()

#Original Image
#sleep(0.5)

camera.capture('/home/pi/Desktop/trial_images/image.jpg')


