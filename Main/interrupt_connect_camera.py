<<<<<<< HEAD
import serial
import time
import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
# from camera import get_error

port = '/dev/ttyACM0'
ser = serial.Serial(port, 115200)
time.sleep(3) # arduino needs time to set up serial


def python_read_line():
    if(ser.in_waiting >0):
        line = ser.readline()
        return line

def get_l_pwm(v_cps):
        return int( (v_cps + 12)/0.148)
# get pwm for velocity
def get_r_pwm(v_cps):
        return int( (v_cps + 15.2)/0.169)
		
# return velocity_left_wheel,velocity_right_wheel to achieve v_ref with that ratio
def desired_velocity(c_ratio, v_ref):
        v_right = (2*c_ratio*v_ref)/(c_ratio + 1)
        v_left = (2*v_ref)/(c_ratio + 1)
        return v_left, v_right
		
		
# waits x seconds
def time_wait(seconds):
    time_start = time.time()
    while( (time.time() - time_start) < seconds):
        pass


# returns a double derived theta which is similar to the velocity added to right wheel and removed from left wheel
# when the car is pointed to the right, aka need a increase speed to R and decrease in L to fix
# will see a positive error since midpoint - (a point < midpoint)
# positive error * -K results in a negative cam_ddot
# therefore we subtract neg from right and add negative to thet left
def PD_error_camera(camera_error, camera_ref, K, B):
    global prev_error
    cam_ddot = -K*(camera_error - camera_ref) - B*(camera_error-prev_error)
    prev_error = camera_error
    return cam_ddot

# return velocity_left_wheel,velocity_right_wheel to achieve v_ref with that ratio


def stop():
    i = 0
    while (i < 10):

        message = python_read_line()
        if message!=None:
            if (len(message) > 15):
                curr_odom = interpret_odom(message)

        # print(pd_error)
        C = 1
        velocity_ref = 0
        desired_l, desired_r = desired_velocity(C, velocity_ref)
        l_pwm = get_l_pwm(desired_l)
        r_pwm = get_r_pwm(desired_r)

        s = str(0)+','+str(0)+'\n'.encode()
        print(s)
        ser.write(s)
        i = i + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def run_straight_x_visual(ref):

    # send inital velocities to arduino of wait to set the wheel pwms
    C = 1
    velocity_ref = 5
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
    print(s)
    ser.write(s)
    # while we havent reached out goal
    # every 100 milliseconds, poll the arduino for latest wheel turn counts
    # get how much the wheels actually turned
    # get distances for each wheel traversed
    # update our odometer readings
    # get a pd error from new thetas
    # update new velocities
    # send new pwms to achieve those velocities to arduino



    #while (curr_odom[0] < goal):
        # wait
    poll_time = 0.1 #in seconds
    time_wait(poll_time)

        # update change left and right wheel
        l_w_turns,r_w_turns = get_wheel_turns()
        #print(curr_odom)

        l_distance = get_distance(l_w_turns)
        # l_wheel_cps = ldistance / poll_time

        r_distance = get_distance(r_w_turns)
        # l_wheel_cps = r_distance / poll_time

        delta_left = l_distance
        delta_right = r_distance

        # update odometer x,y,theta
        update_cord(delta_left, delta_right)

        # get pd error from updated thetas
        # curr_theta = curr_odom[2]

        # function from camera
        curr_visual_error = get_error()
        # since we're talking about pixels here the error could reasonably be [-30,30]
        # approx_velocity = PD_error(curr_visual_error, ref, K=.5, B=0.1)
        approx_velocity = PD_error_camera(curr_visual_error, camera_ref = 0, K=0.5, 0.1)

        r_velocity = r_velocity - approx_velocity
        l_velocity = l_velocity + approx_velocity

        # send the new pwms
        l_pwm = get_l_pwm(l_velocity)
        r_pwm = get_r_pwm(r_velocity)

        s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
        ser.write(s)

## CAMERA STUFF
camera = PiCamera()
rawCapture = PiRGBArray(camera)
rawCapture.truncate(0)
#640 width 480 height
camera_midpoint = 320
white_offset = 100
tolerance = 40
width = 400 #will change
prev_error = 0

def isYellow(array):
    if (array[0] < 200 and array[1] > 200 and array[2] > 200):
        return True

def isWhite(array):
    if (array[0] > 200 and array[1] > 200 and array[2] > 200):
        return True

def isRed(array):
    if (array[0] < 150 and array[1] < 150 and array[2] > 200):
        return True

def get_visual_error():
    global width
    red_seen = False
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    # 345-275 = 70
    crop = image[275:345,0:640]

    # init the yellow and white cord to -1,-1 
    yellow = [-1,-1]
    white = [-1,-1]
    
    # find the yellow pixel 
    for y in range(69,0,-1): #for every row
        for x in range(320,0,-1): # for every column
            if (isRed(crop[y,x])):
                red_seen = True
            if (isYellow(crop[y,x])):
                yellow = [y,x]
                break

    # search for th white pixel in same row of yellow. theoretical should always find one
    line = yellow[0]
    for x in range(320,640):
        if (isWhite(crop[line,x])):
            white = [line,x]
            break

    midpoint = (white[1] + yellow[1])/2

    # if no yellow, pad white by width/2 to be the midponit 
    if (yellow[0] == -1 and yellow[1] == -1):
        midpoint = white[1] - (width/2)


    error = camera_midpoint - midpoint

    if (yellow[0] != -1):
        width = white[1] - yellow[1]

	# PD_error_camera(error, camera_ref = 0, K = 1, B = 0.1)
		
    if (abs(error) > 100):
        print("IGNORE, meaning camera found white in the left half  ")
    else:
        print(error)

    rawCapture.truncate(0)
    return error
		
		
		
		
		
if __name__ == "__main__":
    ser.flushInput()
#     run_straight_x(50,0)
#     turn_left(np.pi/2)
#     curr_odom = [0,0,0]
#     run_straight_y(2800,0)
    run_straight_x_visual(50,0)
    print(curr_odom)
    stop()
=======
import serial
import time
import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
#from camera import get_error

port = '/dev/ttyACM0'
ser = serial.Serial(port, 115200)
time.sleep(3) # arduino needs time to set up serial


def python_read_line():
    if(ser.in_waiting >0):
        line = ser.readline()
        return line

def get_l_pwm(v_cps):
        return int( (v_cps + 12)/0.148)
# get pwm for velocity
def get_r_pwm(v_cps):
        return int( (v_cps + 15.2)/0.169)
		
# return velocity_left_wheel,velocity_right_wheel to achieve v_ref with that ratio
def desired_velocity(c_ratio, v_ref):
        v_right = (2*c_ratio*v_ref)/(c_ratio + 1)
        v_left = (2*v_ref)/(c_ratio + 1)
        return v_left, v_right
		
		
# waits x seconds
def time_wait(seconds):
    time_start = time.time()
    while( (time.time() - time_start) < seconds):
        pass


# returns a double derived theta which is similar to the velocity added to right wheel and removed from left wheel
def PD_error_camera(camera_error, camera_ref, K, B):
    global prev_error
    cam_ddot = -K*(camera_error - camera_ref) - B*(camera_error-prev_error)
    prev_error = camera_error
    print(camera_error)
    return cam_ddot

# return velocity_left_wheel,velocity_right_wheel to achieve v_ref with that ratio


def stop():
    i = 0
    while (i < 10):

        message = python_read_line()
        if message!=None:
            if (len(message) > 15):
                curr_odom = interpret_odom(message)

        # print(pd_error)
        C = 1
        velocity_ref = 0
        desired_l, desired_r = desired_velocity(C, velocity_ref)
        l_pwm = get_l_pwm(desired_l)
        r_pwm = get_r_pwm(desired_r)

        s = str(0)+','+str(0)+'\n'.encode()
        print(s)
        ser.write(s)
        i = i + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

			
			
def run_straight_x_visual(ref):

    # send inital velocities to arduino of wait to set the wheel pwms
    C = 1
    velocity_ref = 4
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
    print(s)
    ser.write(s)
    # while we havent reached out goal
    # every 100 milliseconds, poll the arduino for latest wheel turn counts
    # get how much the wheels actually turned
    # get distances for each wheel traversed
    # update our odometer readings
    # get a pd error from new thetas
    # update new velocities
    # send new pwms to achieve those velocities to arduino



    #while (curr_odom[0] < goal):
        # wait
    poll_time = 0.1 #in seconds
    time_wait(poll_time)

        # update change left and right wheel
        #l_w_turns,r_w_turns = get_wheel_turns()
        #print(curr_odom)

        #l_distance = get_distance(l_w_turns)
        # l_wheel_cps = ldistance / poll_time

        #r_distance = get_distance(r_w_turns)
        # l_wheel_cps = r_distance / poll_time

        #delta_left = l_distance
        #delta_right = r_distance

        # update odometer x,y,theta
        #update_cord(delta_left, delta_right)

        # get pd error from updated thetas
        # curr_theta = curr_odom[2]
    curr_visual_error = get_error()
    approx_velocity = PD_error_camera(curr_visual_error, ref, K=10, B=0.01)

        # # change velocity according to pd error
        # if (r_velocity + approx_velocity) > get_r_cps(160) or (r_velocity + approx_velocity) < get_r_cps(120):

        #     pass
        # else:
        #     r_velocity = r_velocity + approx_velocity
        # if (l_velocity - approx_velocity) > get_l_cps(160) or (l_velocity + approx_velocity) < get_r_cps(120):
        #     pass
        # else:
        #     l_velocity = l_velocity - approx_velocity
    r_velocity = r_velocity - approx_velocity
    l_velocity = l_velocity + approx_velocity
        # send the new pwms
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
    ser.write(s)

## CAMERA STUFF
camera = PiCamera()
rawCapture = PiRGBArray(camera)
rawCapture.truncate(0)
camera_midpoint = 310
white_offset = 100
tolerance = 40
width = 400 #will change
prev_error = 0

def isYellow(array):
    if (array[0] < 200 and array[1] > 200 and array[2] > 200):
        return True

def isWhite(array):
    if (array[0] > 200 and array[1] > 200 and array[2] > 200):
        return True

def isRed(array):
    if (array[0] < 150 and array[1] < 150 and array[2] > 200):
        return True
def get_error():
    global width
    red_seen = False
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    crop = image[275:345,0:640]

    yellow = [-1,-1]
    white = [-1,-1]
    for y in range(69,0,-1):
        for x in range(320,0,-1):
            if (isRed(crop[y,x])):
                red_seen = True
            if (isYellow(crop[y,x])):
                yellow = [y,x]
                break
    line = yellow[0]
    for x in range(320,640):
        if (isWhite(crop[line,x])):
            white = [line,x]
            break

    midpoint = (white[1] + yellow[1])/2


    if (yellow[0] == -1 and yellow[1] == -1):
        midpoint = white[1] - (width/2)

    error = camera_midpoint - midpoint

    if (yellow[0] != -1):
        width = white[1] - yellow[1]

	PD_error_camera(error, camera_ref = 0, K = 1, B = 0.1)
		
    if (abs(error) > 100):
        print("IGNORE")
    else:
        print(error)

    rawCapture.truncate(0)
    return error
		
		
		
		
		
if __name__ == "__main__":
    while 1:
        ser.flushInput()
#     run_straight_x(50,0)
#     turn_left(np.pi/2)
#     curr_odom = [0,0,0]
#     run_straight_y(2800,0)
        run_straight_x_visual(0)
#    print(curr_odom)
#    stop()

>>>>>>> origin/feature_branch_name
