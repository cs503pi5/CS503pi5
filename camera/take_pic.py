from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture('/home/gandalf_student/Documents/CS503pi5/camera/image2.jpg')
camera.stop_preview()
