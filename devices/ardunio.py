import serial
from utils.config import Config
import time


class Ardunio():

    def __init__(self, port ):
        self.port = port       
        self.connect() 
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.connection, self.connection))


    def connect(self):
        for n in range(5):
            try:
                self.connection = serial.Serial(self.port)
                exit()
            except serial.SerialException as ex:
                print(ex)
                time.sleep(1)
        print("couldn't connect to arduino")
        raise ConnectionError 


    def close_serial_connection(self):
        try:
            self.connection.close()
        except serial.SerialException as ex:
            print("error while closing connection")
            print(ex)


    def send(self, msg):
        try:
            self.connection.write(msg)
        except serial.SerialException as ex:
            print(f"error while sending msg{msg}")
            print(ex)

    def wait_for_trigger(self):
        while True:
            trigger = unicode(self.sio.readline())
            if trigger = "t":
                break