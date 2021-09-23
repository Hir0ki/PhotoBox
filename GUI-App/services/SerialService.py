from PySide2.QtCore import QThread, Signal
from devices.ardunio import Ardunio
import logging


class SerialThread(QThread):
    sendtriggermessage = Signal(bytes)
    button1press = Signal(bytes)
    button2press = Signal(bytes)
    button3press = Signal(bytes)
    button4press = Signal(bytes)

    def __init__(self, port):
        QThread.__init__(self)
        logging.info("Starting trigger thread")
        self.run_thread = True
        self.ardunio = Ardunio(port)

    def __del__(self):
        logging.info("closing trigger thread")
        self.run_thread = False
        self.wait(1)

    def run(self):
        while self.run_thread == True:
            logging.info("waiting for message")
            message = self.ardunio.wait_for_trigger()
            self._send_signal_for_message(message)
            logging.info(f"done sending for message{self.run_thread}")


    def _send_signal_for_message(self, message: bytes):
        logging.info(f"Send signal for message: {message}")
        if message == b"t":
            self.sendtriggermessage.emit(True)
        if message == b"1":
            self.button1press.emit(True)
        if message == b"2":
            self.button2press.emit(True)
        if message == b"3":
            self.button3press.emit(True)
        if message == b"4":
            self.button4press.emit(True)
        return False

    