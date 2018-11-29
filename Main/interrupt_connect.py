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

def python_read_line():
    if(ser.in_waiting >0):
        line = ser.readline()
        return line

def interpret_odom(odometry):
    # expecting x,y
    # if (len(odometry)  15):
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
        spoke_count = interpret_odom(line)
        left_wheel_count = spoke_count[0]
        right_wheel_count = spoke_count[1]

    # get the amount of spokes turned
    l_spoke_turned = l_w_count - l_w_count_prev
    r_spoke_turned = r_w_count - r_w_count_prev
    
    # set prev for future use
    l_w_count_prev = l_w_count
    r_w_count_prev = r_w_count

    return l_spoke_turned,r_spoke_turned

# return a distance for a given number of wheel turns     
def get_distancec(w_turns):
    circumference = 22.32914 #cm
    spoke_length = circumference / 20.0
    return w_turns * spoke_length

# update our odometry reading in the curr_odometer array
def update_cord(delta_left, delta_right){
    s_left = delta_left
    s_right = delta_right
    w_base = 19 # distance from end to end of the board
    d_x = (s_left+s_right)/2
    d_theta = numpy.atan2((s_right-s_left)/2, w_base/2) # is radians

    x_cord,y_cord,theta = curr_odom
    theta = theta + d_theta  
    x_cord = x_cord + d_x*np.cos(theta)
    y_cord = y_cord + d_x*np.sin(theta)

    curr_odom = [x_cord, y_cord, theta]
}

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
    l_velocity, r_velocity = desired_velocity(C, velocity_ref)
    l_pwm = get_l_pwm(l_velocity)
    r_pwm = get_r_pwm(r_velocity)

    s = str(l_pwm)+','+str(r_pwm)+'\n'.encode()
    # print(l_pwm, r_pwm)
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
        poll_time = 0.1 #in seconds
        time_wait(poll_time)

        # update change left and right wheel
        l_w_turns,r_w_turns = get_wheel_turns()

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
        approx_velocity = PD_error(curr_theta, 0)

        # change velocity according to pd error
        r_velocity = r_velocity + approx_velocity
        l_velocity = l_velocity - approx_velocity

        # send the new pwms
        l_pwm = get_l_pwm(l_velocity)
        r_pwm = get_r_pwm(r_velocity)
        s = str(l_pwm)+','+str(r_pwm)+'\n'.encode()
        ser.write(s)


if __name__ == "__main__":
    run_straight_x(90)
    print(curr_odom)

