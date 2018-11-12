import cv2
import math

def red_color(array):
    if (array[2] > 150 and array[0] < 150):
        return True
    return False

def line_coords(image, coords):
    h = image.shape[0]
    w = image.shape[1]

    for x in range(0, w):
        first = False
        for y in range(h-1, 0,-1):
            GBR = image[y, x]
            if (red_color(GBR)):
                coords.append(x)
                coords.append(y)
                first = True

red_line = []

img = cv2.imread("pics/red_line_1.jpg")
crop_img = img[380:440, 20:590]
cv2.imwrite("pics/crop.jpg", crop_img) 

line_coords(crop_img, red_line)

rx0, ry0, rx1, ry1 = red_line[0], red_line[1], red_line[len(red_line)-2], red_line[len(red_line)-1]
print("{} {} {} {}".format(rx0, ry0, rx1, ry1))


rm = float((-ry1)-ry0)/float(rx1-rx0)
rb = ry1 - (rm * rx1)

print ("White:\nSlope: {} \nY-Intercept: {}".format(rm,rb)) 