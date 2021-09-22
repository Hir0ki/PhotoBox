# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PhotoBoothslKdFn.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PhotoBooth(object):
    def setupUi(self, PhotoBooth):
        if not PhotoBooth.objectName():
            PhotoBooth.setObjectName(u"PhotoBooth")
        PhotoBooth.resize(1170, 797)
        PhotoBooth.setAutoFillBackground(False)
        PhotoBooth.setStyleSheet(u"background-color: #444242\n" "")
        self.centralwidget = QWidget(PhotoBooth)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 1)

        PhotoBooth.setCentralWidget(self.centralwidget)

        self.retranslateUi(PhotoBooth)

        QMetaObject.connectSlotsByName(PhotoBooth)

    # setupUi

    def retranslateUi(self, PhotoBooth):
        PhotoBooth.setWindowTitle(
            QCoreApplication.translate("PhotoBooth", u"MainWindow", None)
        )

    # retranslateUi
