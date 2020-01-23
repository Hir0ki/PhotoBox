import serial
from utils.config import Config
import time
import io


class Ardunio:
    def __init__(self, port):
        self.port = port
        print(port)
        self.connect()
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.connection, self.connection))

    def connect(self):
        while True:
            try:
                self.connection = serial.Serial(self.port, baudrate=115200)
                break
            except serial.SerialException as ex:
                print(ex)
                time.sleep(1)

    def close_serial_connection(self):
        try:
            self.connection.close()
        except serial.SerialException as ex:
            print("error while closing connection")
            print(ex)

    def send(self, msg):
        try:
            print("test")
            # self.connection.write(msg)
        except serial.SerialException as ex:
            print(f"error while sending msg{msg}")
            print(ex)

    def wait_for_trigger(self):
        print("waiting for trigger ")
        while True:
            trigger = self.connection.read()
            print(trigger)
            if trigger == b"t":
                break
