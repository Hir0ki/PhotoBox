#!/usr/bin/env python

import sys
import logging


import PhotoBooth as pb
from utils.config import Config
from services import CamaraService, SerialService, SessionService, GraphicsViewerService, ControllerService

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsScene, QGraphicsPixmapItem
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Signal, Slot

config = Config()


class PhotoBooth(QMainWindow, pb.Ui_PhotoBooth):
    
    set_preview_signal: Signal = Signal(bool)
    button_led = Signal(tuple)
    new_session_signal = Signal(str)
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        config.setup_logger()
        self.logger = logging.getLogger()

        self.graphics_view_service = GraphicsViewerService.GraphicsViewService(self.graphicsView, self)
        
        self.SessionService = SessionService.SessionService(self)
        self.SessionService.start_new_session()

        self.controller_service = ControllerService.ControllerService(self, self.graphics_view_service, self.SessionService)
        
        
        self.cameraThread = CamaraService.CameraThread(self.SessionService)
        self.new_session_signal.connect(self.cameraThread.set_session_dir)
        self.cameraThread.session_dir = self.SessionService.session_path
        self.cameraThread.newImage.connect(self.controller_service.draw_new_image)
        self.set_preview_signal.connect(self.cameraThread.set_preview_is_aktive)
        
        self.cameraThread.start()
        
        self.SerialThread = SerialService.SerialThread(config.get_serial_port(), self.controller_service)
        self.SerialThread.sendtriggermessage.connect(self.cameraThread.set_trigger)
        self.SerialThread.button_press.connect(self.handle_button_press)

        self.button_led.connect(self.SerialThread.set_buttons_to_blink)
        self.cameraThread.send_to_arduino.connect(self.SerialThread.send_signal_to_arduino)
        self.cameraThread.send_with_delay.connect(self.SerialThread.send_flash_with_delay)
        self.SerialThread.start()
        self.controller_service.draw_start_view()

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
    

    def new_session(self, session_path):
        self.new_session_signal.emit(session_path)

    @Slot(int)
    def handle_button_press(self,button_number):
        self.controller_service.handle_button_press(button_number)

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
            logging.info("show start view")
            self.controller_service.draw_start_view()
        if event.key() == Qt.Key_F2:
            logging.info("Show preview view")
            self.controller_service.draw_preview_view()
        if event.key() == Qt.Key_F3:
            self.controller_service.draw_qr_view()
            logging.info("Show qr view")
            



if __name__ == "__main__":
    app = QApplication(sys.argv)
    pb = PhotoBooth()
    pb.show()
    sys.exit(app.exec_())
