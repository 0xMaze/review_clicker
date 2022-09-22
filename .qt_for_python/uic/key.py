# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'key.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_SecondWindow(object):
    def setupUi(self, SecondWindow):
        if not SecondWindow.objectName():
            SecondWindow.setObjectName(u"SecondWindow")
        SecondWindow.resize(444, 89)
        self.centralwidget = QWidget(SecondWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 101, 51))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(80, 30, 271, 31))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(360, 20, 71, 51))
        SecondWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SecondWindow)

        QMetaObject.connectSlotsByName(SecondWindow)
    # setupUi

    def retranslateUi(self, SecondWindow):
        SecondWindow.setWindowTitle(QCoreApplication.translate("SecondWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("SecondWindow", u"Your key:", None))
        self.pushButton.setText(QCoreApplication.translate("SecondWindow", u"Check key", None))
    # retranslateUi

