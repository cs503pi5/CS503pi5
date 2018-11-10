import cv2
import math

def euc_distance(array):
    sum = 0
    for i in array:
        sum = sum + (i**2)
    return math.sqrt(sum)

def white_color(array):
    threshold = 190
    if (array[0] > threshold and array[1] > threshold and array[2] > threshold):
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
        for x in range(0, w):
            GBR = image[y, x]
            if (white_color(GBR) and first == False):
                #print("X: ", x, "Y: ", y, "BGR: ", image[y, x])
                coords.append(x)
                coords.append(y)
                first = True


# def yellow_coords(image, coords):
#     h = image.shape[0]
#     w = image.shape[1]

#     for y in range(0, h):
#         first = False
#         for x in range(0, w):
#             GBR = image[y, x]
#             if (yellow_color(GBR) and first == False):
#                 print("X: ", x, "Y: ", y, "BGR: ", image[y, x])
#                 coords.append(x)
#                 coords.append(y)
#                 first = True

white_line = []
yellow_line = []

img = cv2.imread("3.jpg")
crop_img = img[400:440, 50:500]
cv2.imwrite("crop.jpg", crop_img) 

line_coords(crop_img, white_line)
# yellow_coords(crop_img, yellow_line)

x0, y0, x1, y1 = white_line[0], white_line[1], white_line[len(white_line)-2], white_line[len(white_line)-1]
m = float(y1-y0)/float(x1-x0)
b = y1 - (m * x1)

print ("Slope: {} \nY-Intercept: {}".format(m,b)) 
