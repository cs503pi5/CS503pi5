import cv2
#from picamera.array import PiRGBArray
#from picamera import PiCamera
#camera = PiCamera()
#rawCapture = PiRGBArray(camera)
#image = rawCapture.array


image = cv2.imread("imgs/orig1.jpg")

image = image[50:110,120:400]
cv2.imwrite("new.jpg",image)
img = cv2.imread("new.jpg",0)
#width,height = cv2.GetSize(image)
height, width = img.shape[:2]
print(str(height) + ',' + str(width))
