import serial
import time

#counter = 0

port = '/dev/ttyACM0'
ser = serial.Serial(port, 115200)
time.sleep(4) # arduino needs time to set up serial

def interpret_odom(odometry):
	#print("here")
	o = [int(x) for x in odometry.rstrip("\r\n").split(",")]
	#print(odometry)
    	return o
#	print (odometry)

def get_wheel_turns():
	l_w_count = 0
        r_w_count = 0
        l_w_count_prev = 0
        r_w_count_prev = 0

#	counter += 1
#	print("No. of times in get_wheel_turns: " + str(counter))
	while 1:
	#	l_w_count = 0
    	#	r_w_count = 0
	#	l_w_count_prev = 0
	#	r_w_count_prev = 0

		while(ser.in_waiting > 0):
        		line = ser.readline()
#			print("Serial data found")
	       	spoke_count = interpret_odom(line)
 		left_wheel_count = spoke_count[0]
       		right_wheel_count = spoke_count[1]
#		print(str(left_wheel_count) + "," + str(right_wheel_count))
		break
	#print(right_wheel_count)
    	#get the amount of spokes turned

	print("out of while loop")
	l_spoke_turned = left_wheel_count - l_w_count_prev
	r_spoke_turned = right_wheel_count - r_w_count_prev
	print(l_spoke_turned)
	print(r_spoke_turned)

   	#set prev for future use
 	l_w_count_prev = left_wheel_count
 	r_w_count_prev = right_wheel_count
    	return l_spoke_turned,r_spoke_turned

def printSomething():
	#while True:
	l_w_turns,r_w_turns = get_wheel_turns()
	print("here")
	print(l_w_turns)
	print(r_w_turns)

while(1):
	print("Once more")
	printSomething()
#get_wheel_turns()
