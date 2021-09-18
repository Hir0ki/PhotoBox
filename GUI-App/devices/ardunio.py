import serial
import time
import io
import logging

class Ardunio:
    def __init__(self, port):
        self.port = port
        self.logger = logging.getLogger()
        self.connect()
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.connection, self.connection))

    def connect(self):
        while True:
            try:
                self.connection = serial.Serial(self.port, baudrate=115200)
                self.logger.info("Conected to serial device")
                break
            except serial.SerialException as ex:
                self.logger.error(f"Couln't connect to Serial on port: {self.port}", exc_info=ex) 
                time.sleep(1)

    def close_serial_connection(self):
        try:
            self.connection.close()
            self.logger.info("Closed serial connection")
        except serial.SerialException as ex:
            self.logger.error("error while closing connection", exc_info=ex )

    def send(self, msg):
        try:
            self.connection.write(msg)
        except serial.SerialException as ex:
            self.logger.error("error while sending msg: {msg}", exc_info=ex )

    def wait_for_trigger(self):
        self.logger.info("waiting for trigger")
        # irgnore first 
        count = 0

        while count != 21:
            trigger = self.connection.read()
            if trigger != b"":
                count += 1
        
        while True:
            trigger = self.connection.read()
            if trigger == b"t":
                self.logger.info(f"Trigger was set to: {trigger}") 
                break

