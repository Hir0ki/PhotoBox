import logging
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsView,
    QGraphicsTextItem
)
from PySide2.QtGui import QPixmap, QFont
from PySide2.QtCore import Qt
from services.QRCodeService import QRCodeService

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

        self.qr_service:QRCodeService = QRCodeService()

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

    def show_qr_code(self, url):
        pixmap_qr_code = QPixmap.fromImage(self.qr_service.generade_qr_code(url))
        scene = QGraphicsScene()
        
        pixmap_item = QGraphicsPixmapItem(pixmap_qr_code)
        half_window_width = self.photobooth_window.width()/2
        pixmap_item.setX(-half_window_width)
        pixmap_item.setY(-10.0)
        logging.info(f"x: {pixmap_item.x()} y: {pixmap_item.y()}")

        url_item = QGraphicsTextItem(f"Die Bilder können unter der Addresse: \n{url} \ngedownloaded werden")
        url_item.setFont(QFont('Arial', 50))
        url_item.setTextWidth(800)

        scene.addItem(pixmap_item)
        scene.addItem(url_item)
        self.gaphices_viewer.setScene(scene)