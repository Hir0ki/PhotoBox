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

    def create_qr_scene(self, scene, qr_pixel_map, qr_text, backgound_pixmap) :
        
        pixmap_item = QGraphicsPixmapItem(qr_pixel_map)
        
        pixmap_item.setY(100)
        pixmap_item.setX(100)

        background_item = QGraphicsPixmapItem(backgound_pixmap)


        url_item = QGraphicsTextItem(qr_text)
        url_item.setFont(QFont('Arial', 50))
        url_item.setTextWidth(820)
        url_item.setY(450)
        url_item.setX(1150)
        url_item.setZValue(1)
       
        pixmap_item.setZValue(1)
        background_item.setZValue(-1)
        
        scene.addItem(pixmap_item)
        scene.addItem(url_item)
        scene.addItem(background_item)
        

        return scene
    
    def create_start_scene(self, scene, qr_pixel_map):
        text_item = QGraphicsTextItem("Wilkommen zur Photobox bitte den Start Button Drücken")
        text_item.setFont(QFont('Arial', 50))
        pixmap_item = QGraphicsPixmapItem(qr_pixel_map)
        
        scene.addItem(pixmap_item)

        return scene

    def show_scene(self, scene):
        self.gaphices_viewer.setScene(scene)