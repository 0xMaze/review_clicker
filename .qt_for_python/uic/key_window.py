# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'key_window.ui'
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

class Ui_KeyChecker(object):
    def setupUi(self, KeyChecker):
        if not KeyChecker.objectName():
            KeyChecker.setObjectName(u"KeyChecker")
        KeyChecker.resize(444, 89)
        self.centralwidget = QWidget(KeyChecker)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 101, 51))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(80, 30, 271, 31))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(360, 30, 71, 31))
        KeyChecker.setCentralWidget(self.centralwidget)

        self.retranslateUi(KeyChecker)

        QMetaObject.connectSlotsByName(KeyChecker)
    # setupUi

    def retranslateUi(self, KeyChecker):
        KeyChecker.setWindowTitle(QCoreApplication.translate("KeyChecker", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("KeyChecker", u"Your key:", None))
        self.pushButton.setText(QCoreApplication.translate("KeyChecker", u"Check key", None))
    # retranslateUi

