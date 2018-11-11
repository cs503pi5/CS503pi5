#!/user/bin/env python
import serial
port="/dev/ttyACM0"

s1 = serial.Serial(port,9600)
s1.flushInput()

# left wheel cps = 0.166 * pwm - 18.7
# right wheel cps = 0.162 * pwm - 19

# get pwm for velocity
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
	
C = 1 
velocity_ref = 20 # cps

desired_l, desired_r = desired_velocity(C, velocity_ref)
l_pwm = get_l_pwm(desired_l)
r_pwm = get_r_pwm(desired_r)

print(l_pwm)
print(r_pwm)

s1.write(str(l_pwm))
s1.write(str(r_pwm))

