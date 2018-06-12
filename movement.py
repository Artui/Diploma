import time

import serial

ser = None


def get_connection():
    global ser
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 115200
    ser.open()
    return ser


def close_connection():
    ser.close()


def start_wheel(index, speed):
    global ser
    str_to_send = "M" + str(index) + speed
    if ser:
        for i in str_to_send:
            time.sleep(0.1)
            ser.write(bytes(i))


def turn_right():
    pass


def turn_left():
    pass


def start_all_wheels(speed):
    for i in range(1, 5):
        start_wheel(i, speed)


def stop_wheel(index):
    global ser
    if ser:
        for i in ["M", str(index), "+", "0", "0", "0"]:
            time.sleep(0.1)
            ser.write(bytes(i))


def stop_all_wheels():
    for i in range(1, 5):
        stop_wheel(i)
