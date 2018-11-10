from picamera import PiCamera
from time import sleep

camera = PiCamera()

def capture_picture(num):
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/Desktop/image.jpg'+str(num))
    camera.stop_preview()
