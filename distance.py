import serial

ser = None


def get_connection():
    global ser
    if not ser:
        ser = serial.Serial()
        ser.port = "/dev/ttyACM0"
        ser.baudrate = 115200
        ser.open()
    return ser


def close_connection():
    ser.close()


def get_distance_lists():
    data = ser.read(100)
    data_int = [ord(val) for val in data]
    glob_temp, temp = [], []
    for i in data_int:
        if i == 36 and len(temp) == 0:
            temp = [i]
        else:
            temp.append(i)
            if len(temp) == 8:
                glob_temp.append(temp)
                temp = []
    return glob_temp[0] if glob_temp else None
