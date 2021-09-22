#!/usr/bin/env python

import sys
import logging


import PhotoBooth as pb
from utils.config import Config
from services import CamaraService, SerialService, SessionService, GraphicsViewerService, ControllerService

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

        self.graphics_view_service = GraphicsViewerService.GraphicsViewService(self.graphicsView, self)
        
        self.SessionService = SessionService.SessionService()
        self.SessionService.start_new_session()
        
        self.cameraThread = CamaraService.CameraThread()
        self.cameraThread.session_dir = self.SessionService.session_path
        self.cameraThread.newImage.connect(self.graphics_view_service.show_new_image)
        self.set_preview_signal.connect(self.cameraThread.set_preview_is_aktive)
        self.cameraThread.start()
        

        self.SerialThread = SerialService.SerialThread(config.get_serial_port())
        self.SerialThread.sendtriggermessage.connect(self.cameraThread.set_trigger)
        self.SerialThread.start()

        self.controller_service = ControllerService.ControllerService(self)

        self.showFullScreen()

    def resizeEvent(self, event):
        
        # handel graphics resize
        if not self.graphics_view_service.pixmap is None:
            
            self.graphics_view_service.pixmap.scaled(
                self.graphicsView.width(),self.graphicsView.height(),Qt.KeepAspectRatio
            )
        self.graphics_view_service.gaphices_viewer.setGeometry(0,0,self.width(),self.height())
        # handel button resize
        self.controller_service.scale_buttons()
        QWidget.resizeEvent(self, event)


    def closeEvent(self, event):
        self.cameraThread.__del__()
        self.SerialThread.__del__()
        event.accept()

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
