import serial
import time
import keyboard

def sendSome():
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.flush()
	
	while True:
			ser.write(b"X0:Y0")

sendSome()
