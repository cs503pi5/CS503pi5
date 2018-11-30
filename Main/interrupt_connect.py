import serial
import time
import numpy as np
import cv2
import math
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera

port = '/dev/ttyACM0'
ser = serial.Serial(port, 115200)
time.sleep(4) # arduino needs time to set up serial

# x,y,theta readings of the car
curr_odom = [0,0,0]

# keep track of previous count of wheel turns for get_wheel_turns fn since arduino only sends total
l_w_count_prev = 0
r_w_count_prev = 0

# keep track of previous theta for pd error and 
theta_prev = 0.0

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
	return int( (v_cps + 18.7)/0.162)

def get_l_cps(pwm):
    return int( 0.184*pwm - 18.7)

def get_r_cps(pwm):
    return int( (0.162*pwm) - 19)

def python_read_line():
    if(ser.in_waiting >0):
        line = ser.readline()
        return line

def interpret_odom(odometry):
    # expecting x,y
    if (len(odometry) > 5):
        # print("intepreted", odometry)
        o = [int(x) for x in odometry.rstrip("\r\n").split(",")]
        return o

# waits x seconds
def time_wait(seconds):
    time_start = time.time()
    while( (time.time() - time_start) < seconds):
        pass

# returns (left wheel turns, right wheel turns)
def get_wheel_turns():

    l_w_count = 0
    r_w_count = 0
    while(ser.in_waiting > 0):
        line = ser.readline()
        print('read in',line)
        if line!=None and (len(line) > 5):
            spoke_count = interpret_odom(line)
            l_w_count = spoke_count[0]
            r_w_count = spoke_count[1]

    # get the amount of spokes turned
    global l_w_count_prev
    global r_w_count_prev

    l_spoke_turned = l_w_count - l_w_count_prev
    r_spoke_turned = r_w_count - r_w_count_prev
    
    # set prev for future use
    l_w_count_prev = l_w_count
    r_w_count_prev = r_w_count 

    return l_spoke_turned,r_spoke_turned

# return a distance for a given number of wheel turns     
def get_distance(w_turns):
    circumference = 22.32914 #cm
    spoke_length = circumference / 20.0
    return w_turns * spoke_length

# update our odometry reading in the curr_odometer array
def update_cord(delta_left, delta_right):
    s_left = delta_left
    s_right = delta_right
    w_base = 19 # distance from end to end of the board
    d_x = (s_left+s_right)/2
    d_theta = np.arctan2((s_right-s_left)/2, w_base/2) # is radians

    global curr_odom
    x_cord,y_cord,theta = curr_odom
    theta = theta + d_theta  
    x_cord = x_cord + d_x*np.cos(theta)
    y_cord = y_cord + d_x*np.sin(theta)

    curr_odom = [x_cord, y_cord, theta]

# returns a double derived theta which is similar to the velocity added to right wheel and removed from left wheel
def PD_error(theta_act, theta_ref, K = 1, B = 0.01):
    global theta_prev
    theta_ddot = -K*(theta_act - theta_ref) - B*(theta_act-theta_prev)
    theta_prev = theta_act
    return theta_ddot   

# return velocity_left_wheel,velocity_right_wheel to achieve v_ref with that ratio
def desired_velocity(c_ratio, v_ref):
	v_right = (2*c_ratio*v_ref)/(c_ratio + 1)
	v_left = (2*v_ref)/(c_ratio + 1)
	return v_left, v_right

# make arduino run straight for a
def run_straight_x(goal):

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
    while (curr_odom[0] < goal):
        # wait 
        poll_time = 0.05 #in seconds
        time_wait(poll_time)

        # update change left and right wheel
        l_w_turns,r_w_turns = get_wheel_turns()
        print(curr_odom)


        l_distance = get_distance(l_w_turns)
        # l_wheel_cps = ldistance / poll_time

        r_distance = get_distance(r_w_turns)
        # l_wheel_cps = r_distance / poll_time

        delta_left = l_distance
        delta_right = r_distance

        # update odometer x,y,theta
        update_cord(delta_left, delta_right)

        # get pd error from updated thetas
        curr_theta = curr_odom[2]
        approx_velocity = PD_error(curr_theta, 0, K=0.1, B=0.01)

        # # change velocity according to pd error
        # if (r_velocity + approx_velocity) > get_r_cps(160) or (r_velocity + approx_velocity) < get_r_cps(120):
        #     pass
        # else:
        #     r_velocity = r_velocity + approx_velocity
        # if (l_velocity - approx_velocity) > get_l_cps(160) or (l_velocity + approx_velocity) < get_r_cps(120):
        #     pass
        # else:
        #     l_velocity = l_velocity - approx_velocity
        r_velocity = r_velocity + approx_velocity
        l_velocity = l_velocity - approx_velocity

        # send the new pwms
        l_pwm = get_l_pwm(l_velocity)
        r_pwm = get_r_pwm(r_velocity)

        s = (str(l_pwm)+','+str(r_pwm)+'\n').encode()
        ser.write(s)

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
    ser.flushInput()
    run_straight_x(80)
    print(curr_odom)
    stop()


