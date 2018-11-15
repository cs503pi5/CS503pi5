
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
	return int( (v_cps + 18.7)/0.166)

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

if __name__ == "__main__":
    print("Stopping...")
    stop()
