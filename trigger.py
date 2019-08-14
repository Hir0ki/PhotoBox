from PySide2.QtCore import QThread, Signal, Slot
from devices.ardunio import Ardunio
import RPi.GPIO as GPIO

class TriggerThread(QThread):
    trigger = Signal(bool)
    def __init__(self, port):
        QThread.__init__(self)
        print("Starting tread")
        self.run_thread = True
        self.ardunio = Ardunio(port)

        self._gpio_setup()
        

    def __del__(self):
        print("closing thread") 
        self.run_thread = False
        self.wait()

    def run(self): 
        
        self.trigger_photo()


    def trigger_photo(self):
        self.ardunio.send(b'T')
        self.sleep(7)
        self.trigger.emit(True)
        self.ardunio.send(b'F')



    def _gpio_setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=self.gpio_trigger_callback, bouncetime=300)  

    
    def gpio_trigger_callback(self, channel):
        self.trigger_photo()


    def wait_for_gpio_pin(self):
        GPIO.wait_for_edge(23, GPIO.RISING)  