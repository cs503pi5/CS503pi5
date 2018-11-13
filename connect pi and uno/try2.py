from time import sleep
import serial
import binascii

err_cnt = 0
ser = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)
print("Hello, waiting for data...")
if ser.isOpen():
	print(ser.name, "is open")
	print(ser)

def Send_Command_To_Pi(message):
	ser.write(message.encode('ascii'))
	sleep(0.2)
	print("Sent")

	sleep(0.1)
	Buffer = ser.inWaiting()
	print("Buffer: ", Buffer)

	try:
		indata = bytes.decode(ser.read())
		print("Read 1")
                print("indata: ", indata)

		indata = indata + bytes.decode(ser.read())
                print("Read 2")
                print("indata: ", indata)

		indata = indata + bytes.decode(ser.read())
                print("Read 3")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 4")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 5")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 6")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 7")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 8")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 9")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 10")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 11")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 12")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 13")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 14")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 15")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 16")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 17")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 18")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 19")
                print("indata: ", indata)

                indata = indata + bytes.decode(ser.read())
                print("Read 20")
                print("indata: ", indata)

		print("Buffer: ", Buffer)

	except:
		err_cnt += 1
		print("ERROR count = ", err_cnt)
		sleep (1)

print("------------------------")
message = "h"
Send_Command_To_Pi(message)

sleep(10)
