## MOTOR METHODS
# hard_straight()
# hard_left()
# hard_right()
# lane_follow()
# high_speed()

import serial
import time
from motor_helpers import *
from stop import*
from camera_functions import*

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
        time_wait(.05)
    stop()

def hard_left():
    C = .2
    velocity_ref = 5
    l_ref_velocity, r_ref_velocity = desired_velocity(C, velocity_ref)
    l_velocity = l_ref_velocity
    r_velocity = r_ref_velocity
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    time_start = time.time()
    while(time.time() < time_start + 6):
        s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
        print(s)
        ser.write(s)
        time_wait(.05)
    stop()


def hard_right():
    C = 10
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
        time_wait(.05)
    stop()

def lane_follow():
    image = take_picture()
    # crop_red = crop_image_for_stop(image)
    # print(at_stop_sign(crop_red))

def high_speed():
    pass