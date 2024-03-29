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
        self.total_count = 0

    def connect(self):
        while True:
            try:
                self.connection = serial.Serial(self.port, baudrate=115200)
                self.logger.info("Conected to serial device")
                break
            except serial.SerialException as ex:
                self.logger.error(
                    f"Couln't connect to Serial on port: {self.port}", exc_info=ex
                )
                time.sleep(1)

    def close_serial_connection(self):
        try:
            self.connection.close()
            self.logger.info("Closed serial connection")
        except serial.SerialException as ex:
            self.logger.error("error while closing connection", exc_info=ex)

    def send(self, msg):
        try:
            self.logger.info(f"sending serial message: {msg}")
            self.connection.write(msg)
        except serial.SerialException as ex:
            self.logger.error("error while sending msg: {msg}", exc_info=ex)

    def wait_for_trigger(self):
        
        # irgnore first
        #self.logger.info(f"waiting for trigger")
        #while self.total_count != 21:
        #    trigger = self.connection.read()
        #    if trigger != b"":
        #        self.total_count += 1

        while True:
            trigger = self.connection.read()
            if trigger == b"t" or trigger in [b"1", b"2", b"3", b"4"]:
                self.logger.info(f"Message from Arduino was set to: {trigger}")
                return trigger
