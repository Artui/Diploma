import serial

ser = None


class Distance:
    def __init__(self):
        pass

    def get_connection(self):
        global ser
        if not ser:
            ser = serial.Serial()
            ser.port = "/dev/ttyACM0"
            ser.baudrate = 115200
            ser.open()
        return ser

    def close_connection(self):
        ser.close()

    def get_distance_list(self):
        data = ser.read(100)
        data_int = [ord(val) for val in data]
        glob_temp, temp = [], []
        for item in data_int:
            if item == 36:
                if len(temp) == 8:
                    glob_temp.append(temp)
                temp = [item]
            else:
                temp.append(item)

        for dist in glob_temp:
            if dist[1] == 83:
                return dist
        return glob_temp[0] if glob_temp else None
