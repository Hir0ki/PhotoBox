import logging
from re import S
from PySide2.QtCore import QSize, QByteArray
from PySide2.QtWidgets import QMainWindow, QGraphicsScene, QPushButton
from PySide2.QtSvg import QSvgRenderer
from utils.config import Config
from PySide2.QtGui import QPixmap, QFont, QIcon 
from services import GraphicsViewerService, SessionService, QRCodeService
from PIL import Image, ImageQt
from pathlib import Path

class ControllerService():
    
    
    # different states: start preview qr_code
    VIEW_START = "start"
    VIEW_PREVIEW = "preview"
    VIEW_QR = "qr_code"

    def __init__(
        self, MainWindow:QMainWindow, GraphicsViewService: GraphicsViewerService.GraphicsViewService, SessionService: SessionService.SessionService, 
    ) -> None:
        self.main_window = MainWindow
        self.grapics_view_service = GraphicsViewService
        self.session_service = SessionService
        self. qr_code_serivce = QRCodeService.QRCodeService()
        self.config = Config()
        self.current_view = self.VIEW_START


    def scale_buttons(self):
        y = int(self.main_window.height() - self.config.get_button_height())
        button_width = int(self.main_window.width() / 4)
        
        self.main_window.pushButton.setGeometry(0,y,button_width,self.config.get_button_height())
        self.main_window.pushButton_2.setGeometry(button_width,y,button_width,self.config.get_button_height())
        self.main_window.pushButton_3.setGeometry(int(button_width*2),y,button_width,self.config.get_button_height())
        self.main_window.pushButton_4.setGeometry(int(button_width*3),y,button_width,self.config.get_button_height())

    def draw_qr_view(self):
        self.current_view = "qr_code"

        scene = QGraphicsScene()
        url = self.config.get_base_url() + self.session_service.session_uuid
        self._clear_all_buttons()
        self._rename_button(self.main_window.pushButton_4,"New Session","")
        self._rename_button(self.main_window.pushButton,"Contiune Session","")
        self.main_window.button_led.emit((True,False,False,True))

        im = Image.open(self.config.get_qr_code_png_path())
        
        pixmap = QPixmap.fromImage(ImageQt.ImageQt(im))

        pixmap_qr_code = QPixmap.fromImage(self.qr_code_serivce.generade_qr_code("https://"+ url))
        self.grapics_view_service.create_qr_scene(scene,pixmap_qr_code,url, pixmap)

        self.grapics_view_service.show_scene(scene)

    def draw_preview_view(self):
        self.current_view = "preview"
        self.main_window.set_preview_signal.emit(True)
        
        self._clear_all_buttons()
        self._rename_button(self.main_window.pushButton_4,"Take Picture","")
        self._rename_button(self.main_window.pushButton_3,"Finalise Session", "dfdsa")
        self.main_window.button_led.emit((False,False,True,True))
        
    def draw_new_image(self, img):
        if self.current_view == "preview":
            self.grapics_view_service.show_new_image(img)
    
    def draw_start_view(self):
        self.current_view = "start"

        self._clear_all_buttons()
        self._rename_button(self.main_window.pushButton_4, "Start","")
        self.main_window.button_led.emit((False,False,False,True))

        scene = QGraphicsScene()

        im = Image.open(self.config.get_start_page_png_path())
        
        pixmap = QPixmap.fromImage(ImageQt.ImageQt(im))

        self.grapics_view_service.create_start_scene(scene, pixmap)

        self.grapics_view_service.show_scene(scene)
    
    def handle_button_press(self,button_number):
        logging.info(f"Button was pressed: {button_number}")

        if self.current_view == self.VIEW_START:
            if button_number == 4:
                self.draw_preview_view()
        
        if self.current_view == self.VIEW_PREVIEW:
            if button_number == 4:
                self.main_window.cameraThread.set_trigger(True)
            if button_number == 3:
                self.draw_qr_view()
        if self.current_view == self.VIEW_QR:
            if button_number == 4:
                self.session_service.start_new_session()
                self.draw_start_view()
            if button_number == 1:
                self.draw_preview_view()

    def _deactivate_button(self, button: QPushButton):
        button.setText("")
    
    def _clear_all_buttons(self):
        self._deactivate_button(self.main_window.pushButton)
        self._deactivate_button(self.main_window.pushButton_2)
        self._deactivate_button(self.main_window.pushButton_3)
        self._deactivate_button(self.main_window.pushButton_4)

    def _rename_button(self, button: QPushButton, text, icon_pixmap):

        button.setText(text)
        button.setFont(QFont('Arial', 25))
    