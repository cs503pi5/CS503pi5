import serial
from time import sleep

s1 = serial.Serial("/dev/ttyACM0",9600)
s1.flushInput()
#write_val = "hello"
#s1.write(write_val.encode('utf-8'))
#s1.flush()
#time.sleep(0.3)
while True:
        s1.write("hello")
#       s1.write((write_val).encode('utf-8'))
#       count = count + 1
        print('written')
	sleep(0.03)
	inputValue=s1.read()
        print(inputValue + '0b10101010')
	sleep(0.03)
