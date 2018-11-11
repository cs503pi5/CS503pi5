from picamera import PiCamera
from time import sleep
import datetime

#Initialize object
camera = PiCamera()

<<<<<<< HEAD:camera/take_pic.py
camera.start_preview()
sleep(5)
camera.capture('/home/gandalf_student/Documents/CS503pi5/camera/image2.jpg')
camera.stop_preview()
=======
#Original Image
#sleep(0.5)
for pic in range(10):
	print(datetime.datetime.now())
	camera.capture('/home/pi/Desktop/trial_images/image' + str(pic) + '.jpg')
#	sleep(0.05)
	print(datetime.datetime.now())
	print('')
>>>>>>> 981ebe06eb7d825441c407692225d56ebe3e948e:camera/camera.py
