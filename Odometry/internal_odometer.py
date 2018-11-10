import numpy as np

#set some variables
delta_right = getRightWheelDistance()
delta_left = getLeftWheelDistance()
wheel_base = 0

delta_x = 0
delta_y = 0

# distance traveled by robot internally
delta_distance_robot = (delta_left + delta_right) / 2

#get internal theta
delta_theta = np.arctan2( delta_distance_robot/ (wheel_base/2) )

# derive cumulative fixed world coord
derived_x = delta_distance_robot * np.cos(delta_theta)
derived_y = delta_distance_robot * np.sin(delta_theta)

delta_x = delta_x + derived_x
delta_y = delta_y + derived_y

