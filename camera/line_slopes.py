import cv2
import math

def euc_distance(array):
    sum = 0
    for i in array:
        sum = sum + (i**2)
    return int(math.sqrt(sum))

# def white_color(array):
#     threshold = 190
#     if (array[0] > threshold and array[1] > threshold and array[2] > threshold):
#         return True
#     return False

def white_color(array):
    if (euc_distance(array) > 300):
        return True
    return False

def yellow_color(array):
    if (euc_distance(array) > 200 and euc_distance(array) < 300):
        return True
    return False

# def yellow_color(array):
#     if (array[0] > 150 and array[1] > 50 and array[2] > 150):
#         print(array)
#         if (array[0] < 200 and array[1] < 80 and array[2] < 200):
#             return True
#     return False

def line_coords(image, coords):
    h = image.shape[0]
    w = image.shape[1]

    for y in range(0, h):
        first = False
        for x in range(w/2, w):
            GBR = image[y, x]
            if (white_color(GBR) and first == False):
                # print("X: ", x, "Y: ", y, "BGR: ", image[y, x])
                coords.append(x)
                coords.append(y)
                first = True


def yellow_coords(image, coords):
    h = image.shape[0]
    w = image.shape[1]/2

    for y in range(0, h):
        first = False
        for x in range(w, 0, -1):
            GBR = image[y, x]
            if (yellow_color(GBR) and first == False):
                # print("X: ", x, "Y: ", y, "BGR: ", image[y, x])
                coords.append(x)
                coords.append(y)
                first = True

def print_img(image):
    h = image.shape[0]
    w = image.shape[1]

    for y in range(0, h):
        for x in range(0, w):
            GBR = image[y, x]
            print(GBR),
        print("\n")

def print_euc(image):
    h = image.shape[0]
    w = image.shape[1]

    for y in range(0, h):
        for x in range(0, w):
            GBR = image[y, x]
            print(euc_distance(GBR)),
        print("\n")


white_line = []
yellow_line = []

img = cv2.imread("3.jpg")
crop_img = img[400:440, 50:500]
cv2.imwrite("crop.jpg", crop_img) 

line_coords(crop_img, white_line)
yellow_coords(crop_img, yellow_line)

wx0, wy0, wx1, wy1 = white_line[0], white_line[1], white_line[len(white_line)-2], white_line[len(white_line)-1]

wm = float((-wy1)-wy0)/float(wx1-wx0)
wb = wy1 - (wm * wx1)

print ("White:\nSlope: {} \nY-Intercept: {}".format(wm,wb)) 

yx0, yy0, yx1, yy1 = yellow_line[0], yellow_line[1], yellow_line[len(yellow_line)-2], yellow_line[len(yellow_line)-1] 

ym = float((-yy1)-yy0)/float(yx1-yx0)
yb = yy1 - (ym * yx1)

print ("Yellow:\nSlope: {} \nY-Intercept: {}".format(ym,yb)) 

midpoint = (wx0 + yx0)/2

print ("Midpoint: {} \nDistance from left: {}".format(midpoint, midpoint-yx0))