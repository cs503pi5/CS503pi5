import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
while True:
	ser.write(b'3')
	ser.write(b'5')
	ser.write(b'7')
#	print("Sent 7")
        if(ser.in_waiting>0):
                line = ser.readline()
                print(line.encode('utf8'))




