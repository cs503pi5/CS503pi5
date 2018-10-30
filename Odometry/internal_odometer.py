# get internal delta
import numpy as np

delta_right_w = 0
delta_left_w = 0
wheel_radius = 0

delta_theta = numpy.arctan2( (delta_right_w-delta_left_w)/wheel_radius)

delta_distance_robot = (delta_left_w + delta_right_w) / 2