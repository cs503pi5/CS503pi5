import serial
from time import sleep

ser = serial.Serial("/dev/ttyACM0",9600)
ser.flushInput()
cnt = 0
while True:
#	cnt = cnt + 1
	ser.write("Hello")
	print("written")
	sleep(0.03)
	print("slept")
#	input = ser.readline()
	#s = input
	sleep(0.03)
	#data_left = ser.inWaiting()
	#input +=ser.read(data_left)
	print(input)
