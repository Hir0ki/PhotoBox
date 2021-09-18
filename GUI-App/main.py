#!/usr/bin/env python

import sys
import logging

import PhotoBooth as pb
from utils.config import Config
from services import CamaraService, ArduinoThread

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt

config = Config()


class PhotoBooth(QMainWindow, pb.Ui_PhotoBooth):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        config.setup_logger()
        self.logger = logging.getLogger()
        self.cameraThread = CamaraService()
        self.cameraThread.newImage.connect(self.newImageDetected)
        self.cameraThread.start()
        self.pushButton.clicked.connect(self.takePicture)
        self.pixmap = None
        if config.get_debug() == "False":
            self.pushButton.hide()
            self.triggerThread = ArduinoThread(config.get_serial_port())
            self.triggerThread.trigger.connect(self.takePicture)
            self.triggerThread.start()

        self.showFullScreen()

    def resizeEvent(self, event):
        if not self.pixmap is None:
            self.label.setPixmap(
                self.pixmap.scaled(
                    self.label.width(), self.label.height(), Qt.KeepAspectRatio
                )
            )

        QWidget.resizeEvent(self, event)

    def takePicture(self, test):
        self.cameraThread.trigger = True
        self.logger.info("set camera trigger property")

    def closeEvent(self, event):
        self.cameraThread.__del__()
        event.accept()

    def newImageDetected(self, img):
        self.pixmap = QPixmap(img)
        self.label.setPixmap(
            self.pixmap.scaled(self.label.width(), self.label.height())
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pb = PhotoBooth()
    pb.show()
    sys.exit(app.exec_())
