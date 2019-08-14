# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhotoBooth.ui',
# licensing of 'PhotoBooth.ui' applies.
#
# Created: Thu Aug 15 00:16:33 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PhotoBooth(object):
    def setupUi(self, PhotoBooth):
        PhotoBooth.setObjectName("PhotoBooth")
        PhotoBooth.resize(663, 421)
        PhotoBooth.setAutoFillBackground(False)
        PhotoBooth.setStyleSheet("background-color: #444242\n"
"")
        self.centralwidget = QtWidgets.QWidget(PhotoBooth)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        PhotoBooth.setCentralWidget(self.centralwidget)

        self.retranslateUi(PhotoBooth)
        QtCore.QMetaObject.connectSlotsByName(PhotoBooth)

    def retranslateUi(self, PhotoBooth):
        PhotoBooth.setWindowTitle(QtWidgets.QApplication.translate("PhotoBooth", "MainWindow", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("PhotoBooth", "Aufnehmen", None, -1))

