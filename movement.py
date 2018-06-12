import time

import serial

ser = None


class Movement:
    ser = None

    def __init__(self):
        self.get_connection()

    def get_connection(self):
        if not self.ser:
            self.ser = serial.Serial()
            self.ser.port = "/dev/ttyUSB0"
            self.ser.baudrate = 115200
            self.ser.open()
        return self.ser

    def close_connection(self):
        self.ser.close()

    def start_wheel(self, index, speed):
        str_to_send = "M" + str(index) + "+" + speed
        print(str_to_send)
        if self.ser:
            for i in str_to_send:
                time.sleep(0.01)
                self.ser.write(bytes(i))

    def start_wheel_back(self, index, speed):
        str_to_send = "M" + str(index) + "-" + speed
        print(str_to_send)
        if self.ser:
            for i in str_to_send:
                time.sleep(0.01)
                self.ser.write(bytes(i))

    def turn_right(self, timeout):
        self.start_wheel(2, '100')
        self.start_wheel_back(1, '100')
        time.sleep(timeout)
        self.stop_wheel(1)
        self.stop_wheel(2)

    def turn_left(self, timeout):
        self.start_wheel(1, '100')
        self.start_wheel_back(2, '100')
        time.sleep(timeout)
        self.stop_wheel(1)
        self.stop_wheel(2)

    def start_all_wheels(self, speed):
        for i in range(1, 5):
            self.start_wheel(i, speed)

    def stop_wheel(self, index):
        if self.ser:
            for i in ["M", str(index), "+", "0", "0", "0"]:
                time.sleep(0.01)
                self.ser.write(bytes(i))

    def stop_all_wheels(self):
        for i in range(1, 5):
            self.stop_wheel(i)
