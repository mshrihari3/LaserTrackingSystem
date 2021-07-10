import serial
import math

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
ser.write(b"X0:Y0")