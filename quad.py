import numpy as np

x = []
y = []
theta = []
x_ini = 0
y_ini = 0
theta_ini = 0

def displacement(s_left, s_right):
        del_x = (s_left + s_right)/2
        del_theta = np.arctan2((s_right - s_left)/2, wheel_base/2) # ?????
        theta_ini += del_theta
        x_ini += (del_x*(np.cos(theta_ini))
        y_ini += (del_x*(np.sin(theta_ini))
        theta.append(theta_ini)
        x.append(x_ini)
        y.append(y_ini)

