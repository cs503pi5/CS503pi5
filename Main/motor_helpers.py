import time

def get_l_pwm(v_cps):
	return int( (v_cps + 12)/0.148)

# get pwm for velocity
def get_r_pwm(v_cps):
	return int( (v_cps + 15.2)/0.150)

def get_l_cps(pwm):
    return int( 0.184*pwm - 18.7)

def get_r_cps(pwm):
    return int( (0.162*pwm) - 19)

def desired_velocity(c_ratio, v_ref):
	v_right = (2*c_ratio*v_ref)/(c_ratio + 1)
	v_left = (2*v_ref)/(c_ratio + 1)
	return v_left, v_right

def time_wait(seconds):
    time_start = time.time()
    while( (time.time() - time_start) < seconds):
        pass