import io

import serial 
import time
import string
import pynmea2

last_known_location={
	'lat': 0,
	'lng': 0
}

def get_gps_location():
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	sio= io.TextIOWrapper(io.BufferedRWPair(ser, ser))

	try:
		line=sio.readline()
		msg=pynmea2.parse(line)
		dic={
			'lat': msg.latitude,
			'lng': msg.longitude
		}
		print(dic)
		global last_known_location
		last_known_location=dic
		return dic
	except serial.SerialException as e:
		print("Device error: {}".format(e))
	except pynmea2.ParseError as e:
		print("Parse error: {}".format(e))
	except Exception as e:
		print("Unknown error: {}".format(e))

	return last_known_location
