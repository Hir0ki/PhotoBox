from PySide2.QtCore import Signal
from PySide2.QtWidgets import QMainWindow, QGraphicsScene
from utils.config import Config
from PySide2.QtGui import QPixmap
from services import GraphicsViewerService, SessionService, QRCodeService

class ControllerService:
    def __init__(
        self, MainWindow:QMainWindow, GraphicsViewService: GraphicsViewerService.GraphicsViewService, SessionService: SessionService.SessionService
    ) -> None:
        self.main_window = MainWindow
        self.grapics_view_service = GraphicsViewService
        self.session_service = SessionService
        self. qr_code_serivce = QRCodeService.QRCodeService()
        self.config = Config()
        # different states: start preview qr_code
        self.current_view = "preview"


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
        text = f"Die Bilder können unter der Addresse: \n{url} \ngedownloaded werden"

        pixmap_qr_code = QPixmap.fromImage(self.qr_code_serivce.generade_qr_code(url))
        self.grapics_view_service.create_qr_scene(scene,pixmap_qr_code,text)

        self.grapics_view_service.show_scene(scene)

    def draw_preview_view(self):
        self.current_view = "preview"
        self.main_window.set_preview_signal.emit(True)
        
    def draw_new_image(self, img):
        if self.current_view == "preview":
            self.grapics_view_service.show_new_image(img)
