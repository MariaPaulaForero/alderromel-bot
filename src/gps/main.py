import serial 
import time
import string
import pynmea2

def get_gps_location():
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata = ser.readline()
 
	if newdata[0:6] == "$GPRMC":
		newmsg=pynmea2.parse(newdata)
		dic = {
			'lat': newmsg.latitude,
			'lng': newmsg.longitude
		}
		return dic