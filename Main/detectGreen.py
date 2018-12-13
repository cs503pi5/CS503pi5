import cv2
#from picamera.array import PiRGBArray
#from picamera import PiCamera
#camera = PiCamera()
#rawCapture = PiRGBArray(camera)
#image = rawCapture.array

red_seen = False
green_seen = False
image = cv2.imread("imgs/orig1.jpg")
#image = cv2.imread("orig1.jpg")
image = image[50:110,120:400]
cv2.imwrite("new.jpg",image)
#img = cv2.imread("new.jpg",0)
#width,height = cv2.GetSize(image)
height, width = image.shape[:2]
#print(str(height) + ',' + str(width))

def isRed(array):
    if(array[0] < 150 and array[1] < 150 and array[2] > 200):
        return True

def isGreen(array):
    if(array[0] > 200 and array[1] > 200 and array[2] > 200):
        return True


def isStop():
    for y in range(height):
        for x in range(width):
            if(isRed(image[y,x])):
	        red_seen = True
	    if(isGreen(image[y,x])):
	        green_seen = True

    if(red_seen and green_seen):
        print("Both red and green seen")
	return True
        #continue with path planner model
    if((red_seen) and (not green_seen)):
        print("Red was seen but no green")
	return False
        #stop 
    if((not red_seen) and (not green_seen)):
        print("Red and green not seen")
	pass
        #continue lane following

if __name__ == "__main__":
    pass
