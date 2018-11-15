def first_fix():
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    cv2.imwrite('full.jpg',image)
    img = image[260:480,420:640]
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('img.jpg',gray)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  
    theta = np.pi / 180  
    threshold = 15  
    min_line_length = 50  
    max_line_gap = 20  
    line_image = np.copy(img) * 0  

    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
    

    slopes = []

    true_lines = []

    for i in range(len(lines[0])):
        arr = lines[0][i]
        m = float(arr[3] - arr[1]) / float(arr[2]-arr[0])
        if (not slope_contains(slopes,m)):
            if (m > .2 or m < -.2):
                slopes.append(m)
                true_lines.append(arr)
        

    print(slopes)
    for line in true_lines:
        x1,y1,x2,y2 = line[0],line[1],line[2],line[3]
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
    
    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

    cv2.imwrite('houghlines.jpg',lines_edges)

    true_lines.sort()




    rawCapture.truncate(0)

