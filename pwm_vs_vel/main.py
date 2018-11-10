#!/user/bin/env python
import serial
port="/dev/ttyACM0"

s1 = serial.Serial(port,9600)
s1.flushInput()

# Passing values from ard to PI included in the string for easy understanding. So have to extract the concatenated value
def ard_2_pi(input_val, keyword):


	try:
		if keyword in input_val:
			return int(input_val[len(keyword):])
		else:
			raise ValueError('incorrect value')
	except ValueError as error:
		print(error.args)
		

while True:
	inputValue=s1.read_until().decode('utf-8')
	print(inputValue)
	
