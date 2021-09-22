# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PhotoBoothlQufxW.ui'
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
        PhotoBooth.resize(663, 421)
        PhotoBooth.setAutoFillBackground(False)
        PhotoBooth.setStyleSheet(u"background-color: #444242\n"
"")
        self.centralwidget = QWidget(PhotoBooth)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_4.addWidget(self.graphicsView)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(30, 50))

        self.horizontalLayout_5.addWidget(self.label_4)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(30, 50))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(30, 50))

        self.horizontalLayout_5.addWidget(self.label_3)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(30, 50))

        self.horizontalLayout_5.addWidget(self.label_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)


        self.gridLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)

        PhotoBooth.setCentralWidget(self.centralwidget)

        self.retranslateUi(PhotoBooth)

        QMetaObject.connectSlotsByName(PhotoBooth)
    # setupUi

    def retranslateUi(self, PhotoBooth):
        PhotoBooth.setWindowTitle(QCoreApplication.translate("PhotoBooth", u"MainWindow", None))
        self.label_4.setText(QCoreApplication.translate("PhotoBooth", u"Button1", None))
        self.label_5.setText(QCoreApplication.translate("PhotoBooth", u"button2", None))
        self.label_3.setText(QCoreApplication.translate("PhotoBooth", u"button", None))
        self.label_2.setText(QCoreApplication.translate("PhotoBooth", u"button", None))
    # retranslateUi

