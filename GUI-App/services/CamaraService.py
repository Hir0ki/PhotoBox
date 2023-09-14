import logging
import time
import cv2

from datetime import  datetime, timedelta

from gphoto2 import camera
from utils.config import Config
from PySide2.QtCore import QThread, Signal, Signal, Slot
from PySide2.QtGui import QImage
from devices.camera import Camera

class CameraThread(QThread):
    newImage: Signal = Signal(QImage)
    send_to_arduino: Signal = Signal(bytes)
    send_with_delay: Signal = Signal(int)
    
    def __init__(self, session_service):
        QThread.__init__(self)
        self.logger = logging.getLogger()
        self.logger.info("Starting camera tread")
        self.run_thread = True
        self.trigger = False
        self.session_dir = None
        self.session_service = session_service
        self.preview_is_aktive = True
        self.camera = Camera()
        self.logger.info("init of camara thread done ")

    @Slot(str)
    def set_session_dir(self, session_dir):
        self.session_dir = session_dir


    def __del__(self):
        self.logger.info("Closing camera thread")
        self.run_thread = False
        self.camera.disconnect_camera()
        self.logger.info("Closed camera")
        self.wait()

    def run(self):
        self.logger.info("starting preview")
        while self.run_thread:
            try: 
                self.camera_loop(self.camera)
            except Exception:
                self.camera = Camera()          
                logging.error("Camera has error")


    def camera_loop(self, camera):
            while self.run_thread:
                if self.preview_is_aktive == True:
                    img = camera.capture_next_preview_as_np_array()
                    self.newImage.emit(self._convert_picture_to_qimage(img))

                    if self.trigger == True:
                        trigger_time = datetime.now()
                        release_time = trigger_time + timedelta(0,Config().get_count_down_time_in_s())
                        self.send_to_arduino.emit(b't')
                        while trigger_time <= release_time:
                            trigger_time = datetime.now()
                            img = camera.capture_next_preview_as_np_array()
                            self.newImage.emit(self._convert_picture_to_qimage(img))
                        self.send_to_arduino.emit(b'f')
                        self.logger.info(f"Saving iamge to dir {self.session_dir}")                    
                        img = camera.capture_image(self.session_dir)
                        cov_img = self._convert_picture_to_qimage(img)
                        self.newImage.emit(cov_img)
                        self.sleep(Config().get_image_show_time_in_s())
                        self.logger.info("Reset trigger porperty")
                        self.trigger = False
            time.sleep(1)
            self.logger.info("deleting camera")
    @Slot(bool)
    def set_trigger(self, state: bool):
        logging.info(f"Trigger state set to: {state}")
        self.trigger = state
        return True

    @Slot(bool)
    def set_preview_is_aktive(self, state: bool):
        self.preview_is_aktive = state
        return True

    def _convert_picture_to_qimage(self, img):
        height, width, channels = img.shape
        if height > 3000 or width > 4000:
            img = cv2.resize(img, (1920, 1080))
            height = 1080
            width = 1920
        res = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = cv2.flip(res, 1)
        #res = cv2.GaussianBlur(res,(15,15),cv2.BORDER_DEFAULT)
        return QImage(res, width, height, width * channels, QImage.Format_RGB888)
