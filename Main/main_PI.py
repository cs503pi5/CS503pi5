#!/user/bin/env python
import serial
import time
port="/dev/ttyACM0"

s1 = serial.Serial(port,9600)
s1.flushInput()

# left wheel cps = 0.166 * pwm - 18.7
# right wheel cps = 0.162 * pwm - 19

# get pwm for velocity
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

# Passing values from ard to PI included in the string for easy understanding. So have to extract the concatenated value
def ard_2_pi(input_val, keyword):


	try:
		if keyword in input_val:
			return int(input_val[len(keyword):])
		else:
			raise ValueError('incorrect value')
	except ValueError as error:
		print(error.args)

def pi_2_ard(case_num, value):
	write_val = str(case_num) + " " + str(value) + "\n"
	s1.write(write_val.encode('utf-8'))
	

# while True:
# 	inputValue=s1.read_until().decode('utf-8')
# 	print(inputValue)
# while True:		
# 	C = 1 
# 	velocity_ref = 0 # cps

# 	desired_l, desired_r = desired_velocity(C, velocity_ref)
# 	l_pwm = get_l_pwm(desired_l)
# 	r_pwm = get_r_pwm(desired_r)

# 	print(l_pwm)
# 	print(r_pwm)

# 	s1.write( (str(l_pwm) + "\n" ).encode('utf-8'))
# 	s1.write( (str(r_pwm) + "\n" ).encode('utf-8'))

# Step 1 Turn in place 

# Step 2 go in a straight line
C = 1
velocity_ref = 5
desired_l, desired_r = desired_velocity(C, velocity_ref)
l_pwm = get_l_pwm(desired_l)
r_pwm = get_r_pwm(desired_r)

print("about to send stuff to pwm")
# left wheel pwm
pi_2_ard(1, l_pwm)
# right wheel pwm
pi_2_ard(2, r_pwm)
# velocity left wheel ref
pi_2_ard(3, desired_l)
# velocity right wheel ref
pi_2_ard(4, desired_r)

print('sent stuff')
x_cord = 0
y_cord = 0
theta = 0

while(x_cord < 24):
	# ping arduino back for x_cord 
	cordinates = s1.read_until('\n')
	x_cord, y_cord, theta = cordinates.split(',')


pi_2_ard(1, 0)
pi_2_ard(2, 0)
