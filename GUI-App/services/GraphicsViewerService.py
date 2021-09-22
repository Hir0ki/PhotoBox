from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsView,
)
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Signal


class GraphicsViewService:
    
    def __init__(
        self, GraphicsViewer: QGraphicsView, PhotoBoothWindow: QMainWindow
    ) -> None:
        self.gaphices_viewer = GraphicsViewer
        self.photobooth_window = PhotoBoothWindow

        # setup graphics View for full screen and no scroll bars 
        self.gaphices_viewer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gaphices_viewer.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)         
        self.gaphices_viewer.setGeometry(0,0,PhotoBoothWindow.width(),PhotoBoothWindow.height())

        self.pixmap = None

    def show_new_image(self, img):
        self.pixmap = QPixmap(img)
        self.pixmap = self.pixmap.scaled(self.gaphices_viewer.width(),self.gaphices_viewer.height(),Qt.KeepAspectRatioByExpanding)
        self.update_pixmap_in_graphics_viewer(self.pixmap)

    def update_pixmap_in_graphics_viewer(self, pixmap: QPixmap):
        self.pixmap = pixmap
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(self.pixmap)
        
        scene.addItem(pixmap_item)
        self.gaphices_viewer.setScene(scene)