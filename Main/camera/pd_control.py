import math 

prev_error = 0

def PD_error_camera(camera_error, K, B):
    global prev_error
    cam_ddot = -K*(camera_error) - B*(camera_error-prev_error)
    prev_error = camera_error
    return cam_ddot

def PD_to_PWM(cam_ddot):
    conversion_factor = 5
    return int(cam_ddot * conversion_factor)
