## MOTOR METHODS
# hard_straight()
# hard_left()
# hard_right()
# lane_follow()
# high_speed()

import serial
import time
from motor_helpers import *
from camera_functions import*
#from stop import *

port = '/dev/ttyACM0'
ser = serial.Serial(port, 115200)

def hard_straight():
    C = 1
    velocity_ref = 5
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    time_start = time.time()
    while(time.time() < time_start + 6):
        s = (str(130)+','+str(150)+'\n').encode()
        print(s)
        ser.write(s)
        time_wait(.1)
    stop()

def hard_left():
    C = 1
    velocity_ref = 5
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    time_start = time.time()
    while(time.time() < time_start + 2):
        s = (str(130)+','+str(150)+'\n').encode()
        print(s)
        ser.write(s)
        time_wait(.1)

    C = 2
    velocity_ref = 8
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    time_start = time.time()
    while(time.time() < time_start + 6.6):
        s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
        print(s)
        ser.write(s)
        time_wait(.1)
    stop()

def hard_right():
    C = 1
    velocity_ref = 5
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    time_start = time.time()
    while(time.time() < time_start + 2):
        s = (str(130)+','+str(150)+'\n').encode()
        print(s)
        ser.write(s)
        time_wait(.1)

    C = .05
    velocity_ref = 5
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    time_start = time.time()
    while(time.time() < time_start + 4):
        s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
        print(s)
        ser.write(s)
        time_wait(.1)
    stop()

# follow the lane
def lane_follow():
    C = 1
    velocity_ref = 10 # default speed is 10
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
    print(s)
    ser.write(s)
    # while not at a stop sign
    # wait every 100ms, take a picture, crop it, and find the visual error
    # pass it through the pd controller and add it each side correspondingly

    is_at_stop_sign = False
    while (not is_at_stop_sign):

        time_start = time.time()
        while( (time.time() - time_start) < 0.1):
            pass
        
        image = take_picture()
        crop_red = crop_image_for_stop(image)
        is_at_stop_sign = at_stop_sign(crop_red)

        crop = crop_image_full_road(image)
        midpoint = find_midpoint(crop)
        visual_error = calculate_error(midpoint)
        approx_velocity = PD_error_camera(visual_error, camera_ref=0, K=.03, B=0.03)
        l_pwm = get_l_pwm(l_velocity + approx_velocity)
        r_pwm = get_r_pwm(r_velocity - approx_velocity)
        s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
        ser.write(s)


def high_speed():
    pass


def stop():
    i = 0
    while (i < 10):
        C = 1
        velocity_ref = 0
        desired_l, desired_r = desired_velocity(C, velocity_ref)
        l_pwm = get_l_pwm(desired_l)
        r_pwm = get_r_pwm(desired_r)

        s = str(0)+','+str(0)+'\n'.encode()
        print(s)
        ser.write(s)
        i = i + 1
        time_wait(.05)