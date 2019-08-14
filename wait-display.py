#!/usr/bin/env python

import sys
import io

from camera import Camera
import time
import cv2
import numpy as np
import gphoto2 as gp
import PhotoBooth as pb
from config import Config

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QThread, Qt, QObject, Signal, Slot

config = Config()

class PhotoBooth(QMainWindow, pb.Ui_PhotoBooth):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.cameraThread = CameraThread()
        self.cameraThread.newImage.connect(self.newImageDetected)
        self.triggerThread = TriggerThread()
        self.triggerThread.trigger.connect(self.takePicture) 
        self.pushButton.clicked.connect(self.takePicture)
        self.pixmap = None
        self.cameraThread.start()
        self.triggerThread.start()
        if config.get_debug() == "False":
            self.pushButton.hide()

    

    def resizeEvent(self, event):
        if not self.pixmap is None:
            self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

        QWidget.resizeEvent(self, event)

    def takePicture(self, test):
        self.cameraThread.trigger = True
        print("set property")



    def closeEvent(self, event):
        self.cameraThread.__del__()
        event.accept()


    def newImageDetected(self, img):
        self.pixmap = QPixmap(img)
        self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

class CameraThread(QThread):
    newImage = Signal(QImage)
    def __init__(self):
        QThread.__init__(self)
        print("Starting tread")
        self.run_thread = True
        self.trigger = False
        self.camera = Camera()

    def __del__(self):
        print("closing thread") 
        self.run_thread = False
        self.camera.disconnect_camera()
        self.wait()

    def run(self): 
        
        
        while self.run_thread:
            # capturing preview and sending it to ui
            img = self.camera.capture_next_preview_as_np_array()
            self.newImage.emit(self._convert_picture_to_qimage(img))

            if self.trigger == True:
                cap_img =  self.camera.capture_image()
                saved_picture = self.camera.save_image(config.get_output_path(), cap_img)
                pixmap = QPixmap(saved_picture)
                
                self.newImage.emit(pixmap.toImage())
                self.sleep(config.get_image_show_time_in_s())
                self.trigger = False
        
        time.sleep(1)
        print("deleting camera")

    def _convert_picture_to_qimage(self, img):
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        height, width, channels = img.shape
        res = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return QImage(res, width, height, width*channels, QImage.Format_RGB888)

class TriggerThread(QThread):
    trigger = Signal(bool)
    def __init__(self):
        QThread.__init__(self)
        print("Starting tread")
        self.run_thread = True

    def __del__(self):
        print("closing thread") 
        self.run_thread = False
        self.wait()

    def run(self): 
        self.sleep(5)
        self.trigger.emit(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pb = PhotoBooth()
    pb.show()
    sys.exit(app.exec_())
