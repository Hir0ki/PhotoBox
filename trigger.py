from PySide2.QtCore import QThread, Signal, Slot
from devices.ardunio import Ardunio
import io
import logging


class TriggerThread(QThread):
    trigger = Signal(bool)

    def __init__(self, port):
        QThread.__init__(self)
        logging.info("Starting trigger tread")
        self.run_thread = True
        self.ardunio = Ardunio(port)


    def __del__(self):
        logging.info("closing trigger thread")
        self.run_thread = False
        self.wait()

    def run(self):
        while self.run_thread == True:
            self.ardunio.wait_for_trigger()
            self.sleep(0.03)
            self.trigger_photo()

    def trigger_photo(self):
        self.ardunio.send(b"T")
        self.trigger.emit(True)
        self.ardunio.send(b"F")
