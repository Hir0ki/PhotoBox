#!/usr/bin/env python

import sys
import io

import time
import cv2
import numpy as np
import gphoto2 as gp
import PhotoBooth as pb

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QThread, Qt, QObject, Signal, Slot

class PhotoBooth(QMainWindow, pb.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.cameraThread = CameraThread()
        self.cameraThread.newImage.connect(self.newImageDetected)
        self.triggerThread = TriggerThread()
        self.triggerThread.trigger.connect(self.takePicture) 
        self.pushButton.clicked.connect(self.takePicture2)
        self.pixmap = None
        self.cameraThread.start()
        self.triggerThread.start()

    
    


    def resizeEvent(self, event):
        if not self.pixmap is None:
            self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

        QWidget.resizeEvent(self, event)

    def takePicture(self, test):
        self.cameraThread.trigger = True
        print("set property")
    
    def takePicture2(self):
        self.cameraThread.trigger = True
        print("set property")
        


    def closeEvent(self, event):
        self.cameraThread.__del__()
        event.accept()


    def newImageDetected(self, img):
        print("New image!")
        self.pixmap = QPixmap(img)
        self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

class CameraThread(QThread):
    newImage = Signal(QImage)
    def __init__(self):
        QThread.__init__(self)
        print("Starting tread")
        self.run_thread = True
        self.trigger = False

    def __del__(self):
        print("closing thread") 
        self.run_thread = False
        self.wait()

    def run(self): 
        camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(camera))
        
        count = 0
        
        while self.run_thread:
            camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
            file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

            ds = io.BytesIO(file_data)
            file_bytes = np.asarray(bytearray(ds.read()), dtype=np.uint8)
            #print(file_bytes)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            #res = cv2.resize(img,None,fx=0.2, fy=0.2, interpolation = cv2.INTER_CUBIC)
            height, width, channels = img.shape
            res = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = QImage(res, width, height, width*channels, QImage.Format_RGB888)
            self.newImage.emit(img)
            if self.trigger == True:
                print("test")
                gp.check_result(gp.gp_camera_trigger_capture(camera))
                self.trigger = False
        gp.gp_camera_get_about(camera)
        
        time.sleep(1)
        #gp.check_result(gp.gp_camera_trigger_capture(camera))
        print("deleting camera")
        #gp.check_result(gp.gp_camera_exit(camera))

        #def convert_gp_img_to_img(self, )

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
