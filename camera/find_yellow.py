import cv2
import numpy as np

img = cv2.imread('crop.jpg')
cv2.imshow('im', img)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('im2', gray)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.imshow('im3', edges)
lines = cv2.HoughLines(edges, 1, np.pi/180, 50)
print(lines)

for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines3.jpg',img)
cv2.imshow('img4',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
