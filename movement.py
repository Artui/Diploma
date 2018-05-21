import serial
import time

ser = None

def get_connection():
	ser = serial.Serial()
	ser.port = "/dev/ttyUSB0"
	ser.baudrate = 155200
	ser.open()
	return ser

def close_connection():
	ser.close()


def start_wheel(index):
	if ser and ser.is_open:
		for i in ["M", str(index), "+", "1", "0", "0"]:
			time.sleep(0.5)
			ser.write(bytes(i))

def start_all_wheels():
	for i in range(1, 5):
		start_wheel(i)

def stop_wheel(index):
	if ser and ser.is_open:
		for i in ["M", str(index), "+", "0", "0", "0"]:
			time.sleep(0.5)
			ser.write(bytes(i))

def stop_all_wheels():
	for i in range(1, 5):
		stop_wheel(i)
			