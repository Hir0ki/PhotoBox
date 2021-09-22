from PySide2.QtCore import Signal
from PySide2.QtWidgets import QMainWindow
from utils.config import Config

class ControllerService:
    def __init__(
        self, MainWindow:QMainWindow
    ) -> None:
        self.main_window = MainWindow
        self.config = Config()


    def scale_buttons(self):
        y = int(self.main_window.height() - self.config.get_button_height())
        button_width = int(self.main_window.width() / 4)
        
        self.main_window.pushButton.setGeometry(0,y,button_width,self.config.get_button_height())
        self.main_window.pushButton_2.setGeometry(button_width,y,button_width,self.config.get_button_height())
        self.main_window.pushButton_3.setGeometry(int(button_width*2),y,button_width,self.config.get_button_height())
        self.main_window.pushButton_4.setGeometry(int(button_width*3),y,button_width,self.config.get_button_height())