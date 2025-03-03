# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSlider,
    QStatusBar, QWidget)
import userUiRescources_rc
import userUiRescources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 768)
        icon = QIcon(QIcon.fromTheme(u"emblem-shared"))
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: rgb(223, 32, 112);")
        self.actionLopeta = QAction(MainWindow)
        self.actionLopeta.setObjectName(u"actionLopeta")
        icon1 = QIcon(QIcon.fromTheme(u"application-exit"))
        self.actionLopeta.setIcon(icon1)
        self.actionKalle = QAction(MainWindow)
        self.actionKalle.setObjectName(u"actionKalle")
        self.actionVille = QAction(MainWindow)
        self.actionVille.setObjectName(u"actionVille")
        self.actionJaana = QAction(MainWindow)
        self.actionJaana.setObjectName(u"actionJaana")
        self.actionMikko = QAction(MainWindow)
        self.actionMikko.setObjectName(u"actionMikko")
        self.actionTallenna_nimell = QAction(MainWindow)
        self.actionTallenna_nimell.setObjectName(u"actionTallenna_nimell")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ssnLineEdit = QLineEdit(self.centralwidget)
        self.ssnLineEdit.setObjectName(u"ssnLineEdit")
        self.ssnLineEdit.setEnabled(True)
        self.ssnLineEdit.setGeometry(QRect(60, 330, 191, 31))
        font = QFont()
        font.setPointSize(18)
        self.ssnLineEdit.setFont(font)
        self.ssnLineEdit.setStyleSheet(u"background-color: rgb(255, 255, 127);\n"
"color: rgb(32, 75, 70);")
        self.ssnLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ssnLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ssnLineEdit.setClearButtonEnabled(True)
        self.keyBarcodeLineEdit = QLineEdit(self.centralwidget)
        self.keyBarcodeLineEdit.setObjectName(u"keyBarcodeLineEdit")
        self.keyBarcodeLineEdit.setEnabled(True)
        self.keyBarcodeLineEdit.setGeometry(QRect(360, 330, 181, 31))
        self.keyBarcodeLineEdit.setFont(font)
        self.keyBarcodeLineEdit.setStyleSheet(u"background-color: rgb(255, 255, 127);")
        self.keyBarcodeLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.keyBarcodeLineEdit.setClearButtonEnabled(True)
        self.takeCarPushButton = QPushButton(self.centralwidget)
        self.takeCarPushButton.setObjectName(u"takeCarPushButton")
        self.takeCarPushButton.setGeometry(QRect(10, 0, 371, 101))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.takeCarPushButton.setFont(font1)
        self.takeCarPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.takeCarPushButton.setToolTipDuration(3000)
        self.takeCarPushButton.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(140, 51, 85);")
        icon2 = QIcon()
        icon2.addFile(u":/pictures/uiPictures/ota.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.takeCarPushButton.setIcon(icon2)
        self.takeCarPushButton.setIconSize(QSize(42, 42))
        self.keyPictureLabel = QLabel(self.centralwidget)
        self.keyPictureLabel.setObjectName(u"keyPictureLabel")
        self.keyPictureLabel.setEnabled(True)
        self.keyPictureLabel.setGeometry(QRect(330, 160, 201, 141))
        self.keyPictureLabel.setPixmap(QPixmap(u":/pictures/uiPictures/keys.png"))
        self.keyPictureLabel.setScaledContents(True)
        self.lenderPictureLabel = QLabel(self.centralwidget)
        self.lenderPictureLabel.setObjectName(u"lenderPictureLabel")
        self.lenderPictureLabel.setEnabled(True)
        self.lenderPictureLabel.setGeometry(QRect(50, 100, 211, 231))
        self.lenderPictureLabel.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.lenderPictureLabel.setPixmap(QPixmap(u":/pictures/uiPictures/Teacher.png"))
        self.lenderPictureLabel.setScaledContents(False)
        self.dateLabel = QLabel(self.centralwidget)
        self.dateLabel.setObjectName(u"dateLabel")
        self.dateLabel.setEnabled(True)
        self.dateLabel.setGeometry(QRect(80, 510, 221, 41))
        font2 = QFont()
        font2.setPointSize(28)
        self.dateLabel.setFont(font2)
        self.dateLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.returnCarPushButton = QPushButton(self.centralwidget)
        self.returnCarPushButton.setObjectName(u"returnCarPushButton")
        self.returnCarPushButton.setGeometry(QRect(440, 0, 371, 101))
        self.returnCarPushButton.setFont(font1)
        self.returnCarPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.returnCarPushButton.setToolTipDuration(3000)
        self.returnCarPushButton.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(140, 51, 85);")
        icon3 = QIcon()
        icon3.addFile(u":/pictures/uiPictures/palauta.drawio.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.returnCarPushButton.setIcon(icon3)
        self.returnCarPushButton.setIconSize(QSize(42, 42))
        self.calendarLabel = QLabel(self.centralwidget)
        self.calendarLabel.setObjectName(u"calendarLabel")
        self.calendarLabel.setGeometry(QRect(40, 500, 31, 51))
        self.calendarLabel.setPixmap(QPixmap(u":/pictures/uiPictures/calendar.png"))
        self.calendarLabel.setScaledContents(True)
        self.timeLabel = QLabel(self.centralwidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setEnabled(True)
        self.timeLabel.setGeometry(QRect(100, 580, 111, 41))
        self.timeLabel.setFont(font2)
        self.timeLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.clockLabel = QLabel(self.centralwidget)
        self.clockLabel.setObjectName(u"clockLabel")
        self.clockLabel.setGeometry(QRect(40, 580, 41, 41))
        self.clockLabel.setPixmap(QPixmap(u":/pictures/uiPictures/clock.png"))
        self.clockLabel.setScaledContents(True)
        self.goBackPushButton = QPushButton(self.centralwidget)
        self.goBackPushButton.setObjectName(u"goBackPushButton")
        self.goBackPushButton.setGeometry(QRect(840, 440, 171, 91))
        font3 = QFont()
        font3.setPointSize(14)
        font3.setBold(True)
        self.goBackPushButton.setFont(font3)
        self.goBackPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.goBackPushButton.setStyleSheet(u"background-color: rgb(140, 51, 85);\n"
"color: rgb(255, 255, 255);")
        icon4 = QIcon()
        icon4.addFile(u":/pictures/uiPictures/back.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.goBackPushButton.setIcon(icon4)
        self.goBackPushButton.setIconSize(QSize(32, 32))
        self.lenderNameLabel = QLabel(self.centralwidget)
        self.lenderNameLabel.setObjectName(u"lenderNameLabel")
        self.lenderNameLabel.setGeometry(QRect(70, 360, 181, 81))
        font4 = QFont()
        font4.setPointSize(16)
        self.lenderNameLabel.setFont(font4)
        self.lenderNameLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lenderNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.carInfoLabel = QLabel(self.centralwidget)
        self.carInfoLabel.setObjectName(u"carInfoLabel")
        self.carInfoLabel.setGeometry(QRect(360, 370, 181, 71))
        font5 = QFont()
        font5.setPointSize(14)
        self.carInfoLabel.setFont(font5)
        self.carInfoLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.carInfoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.okPushButton = QPushButton(self.centralwidget)
        self.okPushButton.setObjectName(u"okPushButton")
        self.okPushButton.setGeometry(QRect(840, 340, 171, 91))
        font6 = QFont()
        font6.setPointSize(24)
        font6.setBold(True)
        self.okPushButton.setFont(font6)
        self.okPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.okPushButton.setStyleSheet(u"background-color: rgb(140, 51, 85);\n"
"color: rgb(255, 255, 255);")
        self.okPushButton.setIconSize(QSize(32, 32))
        self.keyReturnBarcodeLineEdit = QLineEdit(self.centralwidget)
        self.keyReturnBarcodeLineEdit.setObjectName(u"keyReturnBarcodeLineEdit")
        self.keyReturnBarcodeLineEdit.setEnabled(True)
        self.keyReturnBarcodeLineEdit.setGeometry(QRect(360, 330, 181, 31))
        self.keyReturnBarcodeLineEdit.setFont(font)
        self.keyReturnBarcodeLineEdit.setStyleSheet(u"background-color: rgb(255, 255, 127);")
        self.keyReturnBarcodeLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.keyReturnBarcodeLineEdit.setClearButtonEnabled(True)
        self.statusFrame = QFrame(self.centralwidget)
        self.statusFrame.setObjectName(u"statusFrame")
        self.statusFrame.setGeometry(QRect(10, 100, 811, 391))
        self.statusFrame.setFrameShape(QFrame.Shape.Box)
        self.statusFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.statusFrame.setLineWidth(0)
        self.availablePlainTextEdit = QPlainTextEdit(self.statusFrame)
        self.availablePlainTextEdit.setObjectName(u"availablePlainTextEdit")
        self.availablePlainTextEdit.setGeometry(QRect(10, 50, 361, 331))
        font7 = QFont()
        font7.setPointSize(12)
        font7.setBold(True)
        self.availablePlainTextEdit.setFont(font7)
        self.availablePlainTextEdit.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"")
        self.availablePlainTextEdit.setFrameShape(QFrame.Shape.NoFrame)
        self.availablePlainTextEdit.setFrameShadow(QFrame.Shadow.Plain)
        self.availablePlainTextEdit.setLineWidth(4)
        self.availablePlainTextEdit.setMidLineWidth(0)
        self.availablePlainTextEdit.setReadOnly(True)
        self.availablePlainTextEdit.setBackgroundVisible(False)
        self.inUsePlainTextEdit = QPlainTextEdit(self.statusFrame)
        self.inUsePlainTextEdit.setObjectName(u"inUsePlainTextEdit")
        self.inUsePlainTextEdit.setGeometry(QRect(440, 50, 351, 331))
        self.inUsePlainTextEdit.setFont(font7)
        self.inUsePlainTextEdit.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);")
        self.inUsePlainTextEdit.setFrameShape(QFrame.Shape.NoFrame)
        self.inUsePlainTextEdit.setFrameShadow(QFrame.Shadow.Plain)
        self.inUsePlainTextEdit.setLineWidth(8)
        self.line = QFrame(self.statusFrame)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(390, 50, 20, 321))
        self.line.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.availableLabel = QLabel(self.statusFrame)
        self.availableLabel.setObjectName(u"availableLabel")
        self.availableLabel.setGeometry(QRect(110, 10, 131, 31))
        self.availableLabel.setFont(font1)
        self.availableLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.availableLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inUseLabel = QLabel(self.statusFrame)
        self.inUseLabel.setObjectName(u"inUseLabel")
        self.inUseLabel.setGeometry(QRect(550, 10, 131, 31))
        self.inUseLabel.setFont(font1)
        self.inUseLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.inUseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setGeometry(QRect(190, 10, 441, 91))
        font8 = QFont()
        font8.setPointSize(36)
        font8.setBold(True)
        self.statusLabel.setFont(font8)
        self.statusLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.soundCheckBox = QCheckBox(self.centralwidget)
        self.soundCheckBox.setObjectName(u"soundCheckBox")
        self.soundCheckBox.setGeometry(QRect(870, 20, 81, 61))
        font9 = QFont()
        font9.setPointSize(9)
        self.soundCheckBox.setFont(font9)
        self.soundCheckBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.soundCheckBox.setAutoFillBackground(False)
        self.soundCheckBox.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"\n"
"")
        icon5 = QIcon(QIcon.fromTheme(u"audio-volume-medium"))
        self.soundCheckBox.setIcon(icon5)
        self.soundCheckBox.setIconSize(QSize(64, 64))
        self.vehiclePictureLabel = QLabel(self.centralwidget)
        self.vehiclePictureLabel.setObjectName(u"vehiclePictureLabel")
        self.vehiclePictureLabel.setGeometry(QRect(270, 440, 341, 241))
        self.vehiclePictureLabel.setPixmap(QPixmap(u"uiPictures/OXZ915.png"))
        self.vehiclePictureLabel.setScaledContents(True)
        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(880, 150, 51, 22))
        self.horizontalSlider.setMaximum(1)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(810, 130, 61, 81))
        self.label.setPixmap(QPixmap(u"uiPictures/muted.png"))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(940, 140, 61, 71))
        self.label_2.setPixmap(QPixmap(u"uiPictures/unmuted.png"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 33))
        self.menubar.setStyleSheet(u"background-color: rgb(0, 33, 72);\n"
"color: rgb(255, 255, 255);")
        self.menuTiedosto = QMenu(self.menubar)
        self.menuTiedosto.setObjectName(u"menuTiedosto")
        self.menuEdelliset = QMenu(self.menuTiedosto)
        self.menuEdelliset.setObjectName(u"menuEdelliset")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setFont(font9)
        self.statusbar.setToolTipDuration(-1)
        self.statusbar.setStyleSheet(u"background-color: rgb(243, 89, 148);")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuTiedosto.menuAction())
        self.menuTiedosto.addAction(self.actionLopeta)
        self.menuTiedosto.addAction(self.menuEdelliset.menuAction())
        self.menuTiedosto.addAction(self.actionTallenna_nimell)
        self.menuEdelliset.addAction(self.actionKalle)
        self.menuEdelliset.addAction(self.actionVille)
        self.menuEdelliset.addAction(self.actionJaana)
        self.menuEdelliset.addAction(self.actionMikko)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLopeta.setText(QCoreApplication.translate("MainWindow", u"Lopeta", None))
#if QT_CONFIG(shortcut)
        self.actionLopeta.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionKalle.setText(QCoreApplication.translate("MainWindow", u"Kalle", None))
        self.actionVille.setText(QCoreApplication.translate("MainWindow", u"Ville", None))
        self.actionJaana.setText(QCoreApplication.translate("MainWindow", u"Jaana", None))
        self.actionMikko.setText(QCoreApplication.translate("MainWindow", u"Mikko", None))
        self.actionTallenna_nimell.setText(QCoreApplication.translate("MainWindow", u"Tallenna nimell\u00e4...", None))
        self.ssnLineEdit.setText("")
        self.ssnLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Lue ajokortti", None))
        self.keyBarcodeLineEdit.setText("")
        self.keyBarcodeLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Lue avain", None))
#if QT_CONFIG(tooltip)
        self.takeCarPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Tallentaa henkil\u00f6n tiedot tietokantaa</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.takeCarPushButton.setText(QCoreApplication.translate("MainWindow", u"LAINAA", None))
        self.keyPictureLabel.setText("")
        self.lenderPictureLabel.setText("")
        self.dateLabel.setText("")
#if QT_CONFIG(tooltip)
        self.returnCarPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Tallentaa henkil\u00f6n tiedot tietokantaa</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.returnCarPushButton.setText(QCoreApplication.translate("MainWindow", u"PALAUTA", None))
        self.calendarLabel.setText("")
        self.timeLabel.setText("")
        self.clockLabel.setText("")
        self.goBackPushButton.setText(QCoreApplication.translate("MainWindow", u"KUMOA", None))
        self.lenderNameLabel.setText(QCoreApplication.translate("MainWindow", u"Lainaajan nimi", None))
        self.carInfoLabel.setText(QCoreApplication.translate("MainWindow", u"Merkki ja malli", None))
#if QT_CONFIG(tooltip)
        self.okPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Tallentaa tiedot ajop\u00e4iv\u00e4kirjaan</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.okPushButton.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.keyReturnBarcodeLineEdit.setText("")
        self.keyReturnBarcodeLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Lue avain", None))
        self.availablePlainTextEdit.setPlainText("")
        self.inUsePlainTextEdit.setPlainText(QCoreApplication.translate("MainWindow", u"AM-15 Renault Megane 5 henkil\u00f6\u00e4", None))
        self.availableLabel.setText(QCoreApplication.translate("MainWindow", u"VAPAANA", None))
        self.inUseLabel.setText(QCoreApplication.translate("MainWindow", u"AJOSSA", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Tila", None))
        self.soundCheckBox.setText("")
        self.vehiclePictureLabel.setText("")
        self.label.setText("")
        self.label_2.setText("")
        self.menuTiedosto.setTitle(QCoreApplication.translate("MainWindow", u"Tiedosto", None))
        self.menuEdelliset.setTitle(QCoreApplication.translate("MainWindow", u"Edelliset", None))
    # retranslateUi

