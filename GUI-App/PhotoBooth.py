# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PhotoBoothQYTfOk.ui'
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
        #PhotoBooth.setStyleSheet(u"background-color: #444242\n""")
        self.centralwidget = QWidget(PhotoBooth)
        self.centralwidget.setObjectName(u"centralwidget")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(30, 0, 1151, 801))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(40, 740, 121, 51))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(220, 730, 121, 51))
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(440, 720, 121, 51))
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(670, 720, 121, 51))
        self.pushButton_4.setAutoFillBackground(False)
        PhotoBooth.setCentralWidget(self.centralwidget)

        self.retranslateUi(PhotoBooth)

        QMetaObject.connectSlotsByName(PhotoBooth)
    # setupUi

    def retranslateUi(self, PhotoBooth):
        PhotoBooth.setWindowTitle(QCoreApplication.translate("PhotoBooth", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("PhotoBooth", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("PhotoBooth", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("PhotoBooth", u"PushButton", None))
        self.pushButton_4.setText(QCoreApplication.translate("PhotoBooth", u"PushButton", None))
    # retranslateUi

