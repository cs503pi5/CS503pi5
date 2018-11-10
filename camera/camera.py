from picamera import PiCamera
from time import sleep
import datetime

#Initialize object
camera = PiCamera()

#Original Image
#sleep(0.5)
for pic in range(10):
	print(datetime.datetime.now())
	camera.capture('/home/pi/Desktop/trial_images/image' + str(pic) + '.jpg')
#	sleep(0.05)
	print(datetime.datetime.now())
	print('')
