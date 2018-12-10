import serial
import time
import numpy as np
import cv2
import math
import time
import sys

port = '/dev/ttyACM0'
ser = serial.Serial(port, 115200)
#ser = None

l_w_count_prev = 0
r_w_count_prev = 0

def get_l_pwm(v_cps):
	return int( (v_cps + 12)/0.148)

def get_r_pwm(v_cps):
	return int( (v_cps + 15.2)/0.155)  # 15.2, 0.169

def desired_velocity(c_ratio, v_ref):
	v_right = (2*c_ratio*v_ref)/(c_ratio + 1)
	v_left = (2*v_ref)/(c_ratio + 1)
	return v_left, v_right

def run_straight_x_visual(pwm_correction):

    C = 1
    velocity_ref = 5
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    l_pwm = l_pwm - pwm_correction
    r_pwm = r_pwm + pwm_correction

    s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
    print("PWMS:",s)
    ser.write(s)

def run_straight():

    C = 1
    velocity_ref = 5
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
    print("PWMS:",s)
    ser.write(s)
