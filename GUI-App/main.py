#!/usr/bin/env python

import sys
import logging


import PhotoBooth as pb
from utils.config import Config
from services import CamaraService, SerialService, SessionService, ControllerService

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsScene, QGraphicsPixmapItem
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Signal

config = Config()


class PhotoBooth(QMainWindow, pb.Ui_PhotoBooth):
    
    set_preview_signal: Signal = Signal(bool)
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        config.setup_logger()
        self.logger = logging.getLogger()
         

        self.SessionService = SessionService.SessionService()
        self.SessionService.start_new_session()
        
        self.cameraThread = CamaraService.CameraThread()
        self.cameraThread.session_dir = self.SessionService.session_path
        self.cameraThread.newImage.connect(self.newImageDetected)
        self.set_preview_signal.connect(self.cameraThread.set_preview_is_aktive)
        self.cameraThread.start()
        
        self.pixmap = None

        self.SerialThread = SerialService.SerialThread(config.get_serial_port())
        self.SerialThread.sendtriggermessage.connect(self.cameraThread.set_trigger)
        self.SerialThread.start()

        self.showFullScreen()

    def resizeEvent(self, event):
        if not self.pixmap is None:
            self.label.setPixmap(
                self.pixmap.scaled(
                    self.graphicsView.width(),self.graphicsView.height(),Qt.KeepAspectRatio
                )
            )

        QWidget.resizeEvent(self, event)


    def closeEvent(self, event):
        self.cameraThread.__del__()
        self.SerialThread.__del__()
        event.accept()

    def newImageDetected(self, img):
        self.pixmap = QPixmap(img)
        self.pixmap = self.pixmap.scaled(self.graphicsView.width(),self.graphicsView.height(),Qt.KeepAspectRatio)
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(self.pixmap)
        
        scene.addItem(pixmap_item)
        self.graphicsView.setScene(scene)

    def keyPressEvent(self, event):
        """Close application from escape key.
        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_F1:
            logging.info("Set preview to True")
            self.set_preview_signal.emit(True)
        if event.key() == Qt.Key_F2:
            logging.info("Set preview to False")
            self.set_preview_signal.emit(False)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    pb = PhotoBooth()
    pb.show()
    sys.exit(app.exec_())
