import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write(b'3')
ser.write(b'5')
ser.write(b'7')