from path_planner import *
from motor_methods import *
from picamera.array import PiRGBArray
from picamera import PiCamera




def sequenceInterpreter(s):
    if (s == 1):
        pass # 1 - straight connection (Actually never occurs)
    elif (s == 2):
        pass # 2 - straight curved connection right
        hard_straight() # hard code go straight
        lane_follow() # lane follow
        # right turn
        # lane follow
    elif (s == 3):
        pass # 3 - straight curved connection left
        hard_straight()# hard code go straight
        # lane follow
        # left turn
        # lane follow
    elif (s == 4):
        pass # 4 - intersection straight
        hard_straight() # hard code go straight
        lane_follow() # lane follow
    elif (s == 5):
        pass # 5 - intersection right
        hard_right() # hard code right turn
        lane_follow() # lane follow
    elif (s == 6):
        pass # 6 - intersection left
        hard_left() # hard code left turn
        lane_follow() # lane follow
    elif (s == 7):
        pass # 7 - straight speed track inside
        hard_straight() # hard code go straight
        lane_follow() # lane follow
        # right turn
        # high speed
        # right turn
        # lane follow
    elif (s == 8):
        pass # 8 - straight speed track outside
        hard_straight() # hard code go straight
        lane_follow() # lane follow
        # left turn
        # high speed
        # left turn
        # lane follow
    elif (s == 9):
        pass # 9 - intersection speed track inside
        hard_right() # hard code right turn
        lane_follow() # lane follow
        # right turn
        # high speed
        # right turn
        # lane follow
    elif (s == 10):
        pass # 10 - intersection speed track outside
        hard_left() # hard code left turn
        lane_follow() # lane follow
        # left turn
        # high speed
        # left turn
        # lane follow
    elif (s == 11):
        pass # 11 - intersection curved connection right
        hard_right() # hard code right turn
        lane_follow() # lane follow
        # right turn
        # lane follow
    else:
        pass # 12 - intersection curved connection left
        hard_left() # hard code left turn
        lane_follow() # lane follow
        # left turn
        # lane follow


if __name__ == "__main__":
    lane_follow()
    # path = getPath()
    # for s in path:
    #     sequenceInterpreter(s)
    pass
    

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