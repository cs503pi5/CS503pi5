import serial
import time
import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera

## GLOBAL VARIABLES
port = '/dev/ttyACM0'
ser = serial.Serial(port, 115200) #Change port accordingly

camera = PiCamera()
rawCapture = PiRGBArray(camera)

theta_prev = 0

COUNT_ = 30

## COMMUNICATION METHODS
def python_write_string(infoToWrite):
    string_encode = infoToWrite.encode()
    print(string_encode)
    ser.write(string_encode)

def python_read_line():
    if(ser.in_waiting >0):
        line = ser.readline()
        return line

def python_write_pwms(l,r):
    s = str(l)+','+str(r)
    python_write_string(s)

def interpret_odom(odometry):
    if (len(odometry) > 15):
        o = [float(x) for x in odometry.rstrip("\r\n").split(",")]
        return o

## PWM METHODS

# left wheel cps = 0.166 * pwm - 18.7
# right wheel cps = 0.162 * pwm - 19

# get pwm for velocity
# def get_l_pwm(v_cps):
# 	return int( (v_cps + 18.7)/0.184)

# # get pwm for velocity
# def get_r_pwm(v_cps):
# 	return int( (v_cps + 19)/0.162)

def get_l_pwm(v_cps):
	return int( (v_cps + 18.7)/0.184)

# get pwm for velocity
def get_r_pwm(v_cps):
	return int( (v_cps + 19)/0.162)

# return desired velocity for a given v_ref C_ration
def desired_velocity(c_ratio, v_ref):
	v_right = (2*c_ratio*v_ref)/(c_ratio + 1)
	v_left = (2*v_ref)/(c_ratio + 1)
	return v_right, v_left

def PD_error(theta_act, theta_ref, K = 1, B = 0.01):
    global theta_prev
    theta_ddot = -K*(theta_act - theta_ref) - B*(theta_act-theta_prev)
    theta_prev = theta_act
    return theta_ddot   


## CAMERA METHODS
def euc_distance(array):
    sum = 0
    for i in array:
        sum = sum + (i**2)
    return math.sqrt(sum)

def white_color(array):
    if (array[0] > 230 and array[1] > 230 and array[2] > 230):
        return True
    return False

def slope_contains(slopes, slope):
    for i in range(len(slopes)):
        if (slopes[i] - slope < .03 and slopes[i] - slope > -.03):
            return True
    return False

## MAIN METHODS
def init():
    ser.flushInput()
    curr_odom = []

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

def right_turn():
    
    curr_odom = [0,0,0]

    while (curr_odom[2] > -math.pi/2):
        C = 9
        velocity_ref = 7
        desired_l, desired_r = desired_velocity(C, velocity_ref)
        l_pwm = get_l_pwm(desired_l) + 29
        r_pwm = get_r_pwm(desired_r) + 29

        s = str(l_pwm)+','+str(r_pwm)+'\n'.encode()
        print(s)
        ser.write(s)

        message = python_read_line()
        if message!=None:
            if (len(message) > 15):
                curr_odom = interpret_odom(message)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def left_turn(curr_odom_):
    
    curr_odom = curr_odom_

    count = 0
    # while (curr_odom[2] < math.pi/2 - .13):
    while (curr_odom[2] < math.pi/2 - .13):

        if count % 20 == 0: 
            message = python_read_line()
            if message!=None:
                if (len(message) > 15):
                    curr_odom = interpret_odom(message)
            
        if (count % 1000 == 0):
            #before c was 1/80, and pad pwm with 30 and vref 4  
            C = 1.0/2.0
            velocity_ref = 13
            desired_l, desired_r = desired_velocity(C, velocity_ref)
            l_pwm = get_l_pwm(desired_l)
            r_pwm = get_r_pwm(desired_r)
            s = str(l_pwm)+','+str(r_pwm)+'\n'.encode()
            ser.write(s)
            
            print(s)
            print(curr_odom)
            print time.asctime( time.localtime(time.time()) )        
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        count = count+1
    return curr_odom
    


def run_straight_y(distance,curr_odom_):
    pd_error = 0
    curr_odom = curr_odom_
    count = 0

    while (curr_odom[1] < distance):
        message = python_read_line()
        if message!=None:
            if (len(message) > 15):
                curr_odom = interpret_odom(message)
                pd_error = PD_error(curr_odom[2], 0)

        if (count % (COUNT_) == 0):        
            C = 1
            velocity_ref = 5
            desired_l, desired_r = desired_velocity(C, velocity_ref)
            l_pwm = get_l_pwm(desired_l)
            r_pwm = get_r_pwm(desired_r)

            l_pwm = l_pwm - int(pd_error)
            r_pwm = r_pwm + int(pd_error)
            
            l_pwm = 148
            r_pwm = 152
            s = str(l_pwm)+','+str(r_pwm)+'\n'.encode()
            
            ser.write(s)

            print(s)
            print(curr_odom)
            print time.asctime( time.localtime(time.time()) )
        count = count + 1


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return curr_odom

def run_straight_x(distance,curr_odom_):
    count = 0
    message = python_read_line()
    curr_odom = curr_odom_
    if message!=None:
        if (len(message) > 15):
            curr_odom = interpret_odom(message)

    goal = curr_odom[0] + distance
    while (curr_odom[0] < goal):
        message = python_read_line()
        if message!=None:
            if (len(message) > 15):
                curr_odom = interpret_odom(message)

        if (count % (COUNT_) == 0):        
            C = 1
            velocity_ref = 5
            desired_l, desired_r = desired_velocity(C, velocity_ref)
            l_pwm = get_l_pwm(desired_l)
            r_pwm = get_r_pwm(desired_r)

            l_pwm = 147
            r_pwm = 148
            s = str(l_pwm)+','+str(r_pwm)+'\n'.encode()
            ser.write(s)
            print(s)
            print(curr_odom)
            print time.asctime( time.localtime(time.time()) )
        count = count + 1


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return curr_odom
if __name__ == "__main__":
    print("Initializing...")
    init() 
    curr_odom = [0,0,0]
    print("Running straight...")
    curr_odom = run_straight_x(50,curr_odom)
    print("Left turn...")
    curr_odom = left_turn(curr_odom)
    print("Running straight...")
    curr_odom = run_straight_y(130,curr_odom)
    print("Stopping...")
    stop()
    print(curr_odom)
