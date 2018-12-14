from path_planner import *
from motor_methods import *
from picamera.array import PiRGBArray
from picamera import PiCamera
from camera_functions import*

#from detectGreen import isStop

def wait_while_not_green():
    is_at_stop_sign = False
    while(not is_at_stop_sign): # while not not at a stop sign
        time_wait(0.1)
        image = take_picture()
        crop_red = crop_image_for_stop(image)
        is_at_stop_sign = at_stop_sign(crop_red)
 

def sequenceInterpreter(s):
    if (s == 1):
        pass # 1 - straight connection (Actually never occurs)
    elif (s == 2): # 2 - straight curved connection right
        wait_while_not_green()
        hard_straight() # hard code go straight
        lane_follow() # lane follow
        # right turn
        # lane follow
    elif (s == 3):
        # pass # 3 - straight curved connection left
        wait_while_not_green()
        hard_straight()# hard code go straight
        # lane follow
        # left turn
        # lane follow
    elif (s == 4):
        wait_while_not_green()
        hard_straight() # hard code go straight
        lane_follow() # lane follow
        # 4 - intersection straight
        # stopFlag = isStop()
        # while(not stopFlag):
	    # print("Red")
	    # stop()
	    # stopFlag = isStop()
	    #check for stopFlag again
    elif (s == 5):
        wait_while_not_green()
        hard_right() # hard code right turn
        lane_follow() # lane follow
    elif (s == 6):
        wait_while_not_green()
        hard_left() # hard code left turn
        lane_follow() # lane follow
    elif (s == 7):
        wait_while_not_green()
        # pass # 7 - straight speed track inside
        hard_straight() # hard code go straight
        lane_follow() # lane follow
        # right turn
        # high speed
        # right turn
        # lane follow
    elif (s == 8):
        # pass # 8 - straight speed track outside
        wait_while_not_green()
        hard_straight() # hard code go straight
        lane_follow() # lane follow
        # left turn
        # high speed
        # left turn
        # lane follow
    elif (s == 9):
        # pass # 9 - intersection speed track inside
        wait_while_not_green()
        hard_right() # hard code right turn
        lane_follow() # lane follow
        # right turn
        # high speed
        # right turn
        # lane follow
    elif (s == 10):
        # pass # 10 - intersection speed track outside
        wait_while_not_green()
        hard_left() # hard code left turn
        lane_follow() # lane follow
        # left turn
        # high speed
        # left turn
        # lane follow
    elif (s == 11):
        # pass # 11 - intersection curved connection right
        wait_while_not_green()
        hard_right() # hard code right turn
        lane_follow() # lane follow
        # right turn
        # lane follow
    else:
        # pass # 12 - intersection curved connection left
        wait_while_not_green()
        hard_left() # hard code left turn
        lane_follow() # lane follow
        # left turn
        # lane follow


if __name__ == "__main__":
    lane_follow()
    # path = getPath()
    # for s in path:
    #     sequenceInterpreter(s)
    # pass
    

## PATH CONNECTIONS

# 0 - no connection
# 1 - straight connection
# 2 - straight curved connection right
# 3 - straight curved connection left
# 4 - intersection straight
# 5 - intersection right
# 6 - intersection left
# 7 - straight speed track inside
# 8 - straight speed track outside
# 9 - intersection speed track inside
# 10 - intersection speed track outside
# 11 - intersection curved connection right
# 12 - intersection curved connection left

## MOTOR METHODS
# hard_straight()
# hard_left()
# hard_right()
# lane_follow()
# high_speed()
