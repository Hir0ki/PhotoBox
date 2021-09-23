from PySide2.QtCore import QThread, Signal, Slot
from devices.ardunio import Ardunio
import logging


class SerialThread(QThread):
    sendtriggermessage = Signal(bytes)
    button_press = Signal(int)

    def __init__(self, port):
        QThread.__init__(self)
        logging.info("Starting trigger thread")
        self.run_thread = True
        self.ardunio = Ardunio(port)
        self.current_led_state = [False,False,False,False]

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

    @Slot(tuple)
    def set_buttons_to_blink(self,button_tuple):
        
        if button_tuple[0] == True and self.current_led_state[0] == False:
            self.current_led_state[0] = True
        else:
            self.current_led_state[0] = False
        if button_tuple[1]  == True and self.current_led_state[1] == False:
            self.current_led_state[1] = True
        else:
            self.current_led_state[1] = False
        if button_tuple[2]  == True and self.current_led_state[2] == False:
            self.current_led_state[2] = True
        else:
            self.current_led_state[2] = False
        if button_tuple[3]  == True and self.current_led_state[3] == False:
            self.current_led_state[3] = True
        else:
            self.current_led_state[3] = False

        idx = 1
        logging.info(f"sending led state: {self.current_led_state}")
        for entry in self.current_led_state:
            
            if entry == True:
                self.ardunio.send(bytes(str(idx), 'utf-8'))
            else:
                self.ardunio.send(bytes(str(idx+4), 'utf-8'))
            
            idx += 1


    def _send_signal_for_message(self, message: bytes):
        logging.info(f"Send signal for message: {message}")
        if message == b"t":
            self.sendtriggermessage.emit(True)
        if message == b"1":
            self.button_press.emit(1)
        if message == b"2":
            self.button_press.emit(2)
        if message == b"3":
            self.button_press.emit(3)
        if message == b"4":
            self.button_press.emit(4)
        

    