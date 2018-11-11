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
	return int( (v_cps + 19.7)/0.166)

# get pwm for velocity
def get_r_pwm(v_cps):
	return int( (v_cps + 12)/0.162)

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

# left wheel pwm
write_val = "1 " + (str(l_pwm)) + "\n" 
s1.write( write_val.encode('utf-8'))
# right wheel pwm
write_val = "2 " + (str(l_pwm)) + "\n" 
s1.write( write_val.encode('utf-8'))
# velocity left wheel ref
write_val = "3 " + (str(desired_l)) + "\n" 
s1.write( write_val.encode('utf-8'))
# velocity right wheel ref
write_val = "4 " + (str(desired_r)) + "\n" 
s1.write( write_val.encode('utf-8'))

while(x_cord < 24):
	# ping arduino back for x_cord 
	a = 2
