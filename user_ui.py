# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)
import userUiRescources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1318, 939)
        MainWindow.setMinimumSize(QSize(1280, 720))
        MainWindow.setMaximumSize(QSize(1920, 1080))
        icon = QIcon(QIcon.fromTheme(u"emblem-shared"))
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: rgb(223, 32, 112);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.topFrame = QFrame(self.centralwidget)
        self.topFrame.setObjectName(u"topFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topFrame.sizePolicy().hasHeightForWidth())
        self.topFrame.setSizePolicy(sizePolicy)
        self.topFrame.setMinimumSize(QSize(1200, 0))
        self.topFrame.setMaximumSize(QSize(1920, 80))
        self.topFrame.setFrameShape(QFrame.Shape.Box)
        self.topFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout = QHBoxLayout(self.topFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.soundCheckBox = QCheckBox(self.topFrame)
        self.soundCheckBox.setObjectName(u"soundCheckBox")
        self.soundCheckBox.setMaximumSize(QSize(80, 60))
        font = QFont()
        font.setPointSize(9)
        self.soundCheckBox.setFont(font)
        self.soundCheckBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.soundCheckBox.setAutoFillBackground(False)
        self.soundCheckBox.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"\n"
"")
        icon1 = QIcon(QIcon.fromTheme(u"audio-volume-medium"))
        self.soundCheckBox.setIcon(icon1)
        self.soundCheckBox.setIconSize(QSize(64, 64))

        self.horizontalLayout.addWidget(self.soundCheckBox)

        self.logoLabel_3 = QLabel(self.topFrame)
        self.logoLabel_3.setObjectName(u"logoLabel_3")
        sizePolicy.setHeightForWidth(self.logoLabel_3.sizePolicy().hasHeightForWidth())
        self.logoLabel_3.setSizePolicy(sizePolicy)
        self.logoLabel_3.setMinimumSize(QSize(0, 0))
        self.logoLabel_3.setMaximumSize(QSize(60, 60))
        self.logoLabel_3.setPixmap(QPixmap(u"uiPictures/Raseko-logo-pysty_NEGA.png"))
        self.logoLabel_3.setScaledContents(True)

        self.horizontalLayout.addWidget(self.logoLabel_3)


        self.verticalLayout_5.addWidget(self.topFrame)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(1260, 384))
        self.stackedWidget.setFrameShape(QFrame.Shape.Box)
        self.mainPage = QWidget()
        self.mainPage.setObjectName(u"mainPage")
        self.gridLayout_2 = QGridLayout(self.mainPage)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.statusFrame = QFrame(self.mainPage)
        self.statusFrame.setObjectName(u"statusFrame")
        sizePolicy.setHeightForWidth(self.statusFrame.sizePolicy().hasHeightForWidth())
        self.statusFrame.setSizePolicy(sizePolicy)
        self.statusFrame.setMaximumSize(QSize(1200, 1000))
        self.statusFrame.setFrameShape(QFrame.Shape.Box)
        self.statusFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.statusFrame.setLineWidth(1)
        self.gridLayout_3 = QGridLayout(self.statusFrame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(9, 9, 9, 9)
        self.carListFrame = QFrame(self.statusFrame)
        self.carListFrame.setObjectName(u"carListFrame")
        self.carListFrame.setFrameShape(QFrame.Shape.Box)
        self.carListFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_4 = QGridLayout(self.carListFrame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.availablePlainTextEdit_2 = QPlainTextEdit(self.carListFrame)
        self.availablePlainTextEdit_2.setObjectName(u"availablePlainTextEdit_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.availablePlainTextEdit_2.sizePolicy().hasHeightForWidth())
        self.availablePlainTextEdit_2.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.availablePlainTextEdit_2.setFont(font1)
        self.availablePlainTextEdit_2.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"\n"
"")
        self.availablePlainTextEdit_2.setFrameShape(QFrame.Shape.NoFrame)
        self.availablePlainTextEdit_2.setFrameShadow(QFrame.Shadow.Plain)
        self.availablePlainTextEdit_2.setLineWidth(4)
        self.availablePlainTextEdit_2.setMidLineWidth(0)
        self.availablePlainTextEdit_2.setReadOnly(True)
        self.availablePlainTextEdit_2.setBackgroundVisible(False)

        self.gridLayout_4.addWidget(self.availablePlainTextEdit_2, 1, 0, 1, 1)

        self.availableLabel_2 = QLabel(self.carListFrame)
        self.availableLabel_2.setObjectName(u"availableLabel_2")
        font2 = QFont()
        font2.setPointSize(16)
        font2.setBold(True)
        self.availableLabel_2.setFont(font2)
        self.availableLabel_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.availableLabel_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.availableLabel_2, 0, 0, 1, 1)

        self.inUsePlainTextEdit_2 = QPlainTextEdit(self.carListFrame)
        self.inUsePlainTextEdit_2.setObjectName(u"inUsePlainTextEdit_2")
        sizePolicy1.setHeightForWidth(self.inUsePlainTextEdit_2.sizePolicy().hasHeightForWidth())
        self.inUsePlainTextEdit_2.setSizePolicy(sizePolicy1)
        self.inUsePlainTextEdit_2.setFont(font1)
        self.inUsePlainTextEdit_2.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);")
        self.inUsePlainTextEdit_2.setFrameShape(QFrame.Shape.NoFrame)
        self.inUsePlainTextEdit_2.setFrameShadow(QFrame.Shadow.Plain)
        self.inUsePlainTextEdit_2.setLineWidth(8)
        self.inUsePlainTextEdit_2.setReadOnly(True)

        self.gridLayout_4.addWidget(self.inUsePlainTextEdit_2, 1, 3, 1, 1)

        self.inUseLabel_2 = QLabel(self.carListFrame)
        self.inUseLabel_2.setObjectName(u"inUseLabel_2")
        self.inUseLabel_2.setFont(font2)
        self.inUseLabel_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.inUseLabel_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.inUseLabel_2, 0, 3, 1, 1)

        self.line_2 = QFrame(self.carListFrame)
        self.line_2.setObjectName(u"line_2")
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setMaximumSize(QSize(3, 760))
        self.line_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.line_2.setFrameShadow(QFrame.Shadow.Plain)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QFrame.Shape.VLine)

        self.gridLayout_4.addWidget(self.line_2, 1, 2, 1, 1)


        self.gridLayout_3.addWidget(self.carListFrame, 2, 1, 1, 1)

        self.statusLabel = QLabel(self.statusFrame)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy2)
        self.statusLabel.setMaximumSize(QSize(1200, 100))
        font3 = QFont()
        font3.setPointSize(36)
        font3.setBold(True)
        self.statusLabel.setFont(font3)
        self.statusLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.statusLabel, 1, 1, 1, 1)


        self.gridLayout_2.addWidget(self.statusFrame, 7, 0, 1, 1)

        self.topButtonFrame = QFrame(self.mainPage)
        self.topButtonFrame.setObjectName(u"topButtonFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.topButtonFrame.sizePolicy().hasHeightForWidth())
        self.topButtonFrame.setSizePolicy(sizePolicy3)
        self.topButtonFrame.setMaximumSize(QSize(1200, 350))
        self.topButtonFrame.setFrameShape(QFrame.Shape.Box)
        self.topButtonFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.topButtonFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.takeCarPushButton = QPushButton(self.topButtonFrame)
        self.takeCarPushButton.setObjectName(u"takeCarPushButton")
        font4 = QFont()
        font4.setPointSize(42)
        font4.setBold(True)
        self.takeCarPushButton.setFont(font4)
        self.takeCarPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.takeCarPushButton.setToolTipDuration(3000)
        self.takeCarPushButton.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(140, 51, 85);")
        self.takeCarPushButton.setIconSize(QSize(42, 42))
        self.takeCarPushButton.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.takeCarPushButton)

        self.horizontalSpacer = QSpacerItem(60, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.returnCarPushButton = QPushButton(self.topButtonFrame)
        self.returnCarPushButton.setObjectName(u"returnCarPushButton")
        self.returnCarPushButton.setFont(font4)
        self.returnCarPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.returnCarPushButton.setToolTipDuration(3000)
        self.returnCarPushButton.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(140, 51, 85);")
        self.returnCarPushButton.setIconSize(QSize(42, 42))

        self.horizontalLayout_2.addWidget(self.returnCarPushButton)


        self.gridLayout_2.addWidget(self.topButtonFrame, 3, 0, 1, 1)

        self.stackedWidget.addWidget(self.mainPage)
        self.lendPage = QWidget()
        self.lendPage.setObjectName(u"lendPage")
        self.gridLayout_7 = QGridLayout(self.lendPage)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame = QFrame(self.lendPage)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(1200, 80))
        self.frame.setMaximumSize(QSize(1920, 80))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_7 = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)

        self.reasonComboBox = QComboBox(self.frame)
        self.reasonComboBox.setObjectName(u"reasonComboBox")
        sizePolicy2.setHeightForWidth(self.reasonComboBox.sizePolicy().hasHeightForWidth())
        self.reasonComboBox.setSizePolicy(sizePolicy2)
        self.reasonComboBox.setMinimumSize(QSize(600, 0))
        font5 = QFont()
        font5.setPointSize(28)
        font5.setBold(True)
        self.reasonComboBox.setFont(font5)
        self.reasonComboBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.reasonComboBox.setStyleSheet(u"background-color: rgb(255, 255, 127);\n"
"color: rgb(32, 75, 70);")

        self.horizontalLayout_4.addWidget(self.reasonComboBox)

        self.horizontalSpacer_8 = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.lendPage)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QSize(1200, 380))
        self.frame_2.setMaximumSize(QSize(1900, 1000))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_9 = QGridLayout(self.frame_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.timeFrame = QFrame(self.frame_2)
        self.timeFrame.setObjectName(u"timeFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.timeFrame.sizePolicy().hasHeightForWidth())
        self.timeFrame.setSizePolicy(sizePolicy4)
        self.timeFrame.setMinimumSize(QSize(450, 360))
        self.timeFrame.setMaximumSize(QSize(550, 460))
        self.timeFrame.setFrameShape(QFrame.Shape.Box)
        self.timeFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_8 = QGridLayout(self.timeFrame)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.dateLabel = QLabel(self.timeFrame)
        self.dateLabel.setObjectName(u"dateLabel")
        self.dateLabel.setEnabled(True)
        sizePolicy.setHeightForWidth(self.dateLabel.sizePolicy().hasHeightForWidth())
        self.dateLabel.setSizePolicy(sizePolicy)
        self.dateLabel.setMinimumSize(QSize(180, 50))
        self.dateLabel.setMaximumSize(QSize(350, 50))
        font6 = QFont()
        font6.setPointSize(28)
        self.dateLabel.setFont(font6)
        self.dateLabel.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_8.addWidget(self.dateLabel, 0, 1, 1, 1)

        self.calendarLabel = QLabel(self.timeFrame)
        self.calendarLabel.setObjectName(u"calendarLabel")
        sizePolicy2.setHeightForWidth(self.calendarLabel.sizePolicy().hasHeightForWidth())
        self.calendarLabel.setSizePolicy(sizePolicy2)
        self.calendarLabel.setMinimumSize(QSize(50, 50))
        self.calendarLabel.setMaximumSize(QSize(50, 50))
        self.calendarLabel.setPixmap(QPixmap(u":/pictures/uiPictures/calendar.png"))
        self.calendarLabel.setScaledContents(True)

        self.gridLayout_8.addWidget(self.calendarLabel, 0, 0, 1, 1)

        self.timeLabel = QLabel(self.timeFrame)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setEnabled(True)
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)
        self.timeLabel.setMinimumSize(QSize(180, 50))
        self.timeLabel.setMaximumSize(QSize(350, 50))
        self.timeLabel.setFont(font6)
        self.timeLabel.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_8.addWidget(self.timeLabel, 2, 1, 1, 1)

        self.clockLabel = QLabel(self.timeFrame)
        self.clockLabel.setObjectName(u"clockLabel")
        self.clockLabel.setMaximumSize(QSize(50, 50))
        self.clockLabel.setPixmap(QPixmap(u":/pictures/uiPictures/clock.png"))
        self.clockLabel.setScaledContents(True)

        self.gridLayout_8.addWidget(self.clockLabel, 2, 0, 1, 1)


        self.gridLayout_9.addWidget(self.timeFrame, 0, 2, 1, 1)

        self.carRegisterFrame = QFrame(self.frame_2)
        self.carRegisterFrame.setObjectName(u"carRegisterFrame")
        sizePolicy.setHeightForWidth(self.carRegisterFrame.sizePolicy().hasHeightForWidth())
        self.carRegisterFrame.setSizePolicy(sizePolicy)
        self.carRegisterFrame.setMinimumSize(QSize(260, 360))
        self.carRegisterFrame.setMaximumSize(QSize(360, 460))
        self.carRegisterFrame.setFrameShape(QFrame.Shape.Box)
        self.carRegisterFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_5 = QGridLayout(self.carRegisterFrame)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.registerPlateBGLabel = QLabel(self.carRegisterFrame)
        self.registerPlateBGLabel.setObjectName(u"registerPlateBGLabel")
        sizePolicy.setHeightForWidth(self.registerPlateBGLabel.sizePolicy().hasHeightForWidth())
        self.registerPlateBGLabel.setSizePolicy(sizePolicy)
        self.registerPlateBGLabel.setMinimumSize(QSize(180, 50))
        self.registerPlateBGLabel.setMaximumSize(QSize(230, 50))
        self.registerPlateBGLabel.setPixmap(QPixmap(u":/pictures/uiPictures/plateBGPicture.png"))
        self.registerPlateBGLabel.setScaledContents(True)

        self.gridLayout_5.addWidget(self.registerPlateBGLabel, 3, 0, 1, 1)

        self.keyBarcodeLineEdit = QLineEdit(self.carRegisterFrame)
        self.keyBarcodeLineEdit.setObjectName(u"keyBarcodeLineEdit")
        self.keyBarcodeLineEdit.setEnabled(True)
        sizePolicy.setHeightForWidth(self.keyBarcodeLineEdit.sizePolicy().hasHeightForWidth())
        self.keyBarcodeLineEdit.setSizePolicy(sizePolicy)
        self.keyBarcodeLineEdit.setMinimumSize(QSize(180, 50))
        self.keyBarcodeLineEdit.setMaximumSize(QSize(230, 50))
        font7 = QFont()
        font7.setFamilies([u"Trebuchet MS"])
        font7.setPointSize(24)
        font7.setBold(True)
        self.keyBarcodeLineEdit.setFont(font7)
        self.keyBarcodeLineEdit.setStyleSheet(u"background-color: rgb(208, 208, 208);")
        self.keyBarcodeLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.keyBarcodeLineEdit.setClearButtonEnabled(True)

        self.gridLayout_5.addWidget(self.keyBarcodeLineEdit, 4, 0, 1, 1)

        self.keyPictureLabel = QLabel(self.carRegisterFrame)
        self.keyPictureLabel.setObjectName(u"keyPictureLabel")
        self.keyPictureLabel.setEnabled(True)
        sizePolicy.setHeightForWidth(self.keyPictureLabel.sizePolicy().hasHeightForWidth())
        self.keyPictureLabel.setSizePolicy(sizePolicy)
        self.keyPictureLabel.setMinimumSize(QSize(180, 180))
        self.keyPictureLabel.setMaximumSize(QSize(210, 210))
        self.keyPictureLabel.setPixmap(QPixmap(u":/pictures/uiPictures/keys.png"))
        self.keyPictureLabel.setScaledContents(True)

        self.gridLayout_5.addWidget(self.keyPictureLabel, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.carRegisterFrame, 0, 1, 1, 1)

        self.lenderInfoFrame = QFrame(self.frame_2)
        self.lenderInfoFrame.setObjectName(u"lenderInfoFrame")
        sizePolicy.setHeightForWidth(self.lenderInfoFrame.sizePolicy().hasHeightForWidth())
        self.lenderInfoFrame.setSizePolicy(sizePolicy)
        self.lenderInfoFrame.setMinimumSize(QSize(260, 360))
        self.lenderInfoFrame.setMaximumSize(QSize(360, 460))
        self.lenderInfoFrame.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lenderInfoFrame.setAutoFillBackground(False)
        self.lenderInfoFrame.setFrameShape(QFrame.Shape.Box)
        self.lenderInfoFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.lenderInfoFrame.setLineWidth(1)
        self.gridLayout_10 = QGridLayout(self.lenderInfoFrame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.lenderPictureLabel = QLabel(self.lenderInfoFrame)
        self.lenderPictureLabel.setObjectName(u"lenderPictureLabel")
        self.lenderPictureLabel.setEnabled(True)
        sizePolicy.setHeightForWidth(self.lenderPictureLabel.sizePolicy().hasHeightForWidth())
        self.lenderPictureLabel.setSizePolicy(sizePolicy)
        self.lenderPictureLabel.setMinimumSize(QSize(180, 180))
        self.lenderPictureLabel.setMaximumSize(QSize(210, 210))
        self.lenderPictureLabel.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.lenderPictureLabel.setPixmap(QPixmap(u":/pictures/uiPictures/Teacher.png"))
        self.lenderPictureLabel.setScaledContents(False)

        self.gridLayout_10.addWidget(self.lenderPictureLabel, 0, 0, 1, 1)

        self.lenderNameLabel = QLabel(self.lenderInfoFrame)
        self.lenderNameLabel.setObjectName(u"lenderNameLabel")
        sizePolicy.setHeightForWidth(self.lenderNameLabel.sizePolicy().hasHeightForWidth())
        self.lenderNameLabel.setSizePolicy(sizePolicy)
        self.lenderNameLabel.setMinimumSize(QSize(180, 50))
        self.lenderNameLabel.setMaximumSize(QSize(230, 50))
        self.lenderNameLabel.setFont(font7)
        self.lenderNameLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lenderNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lenderNameLabel, 1, 0, 1, 1)

        self.ssnLineEdit = QLineEdit(self.lenderInfoFrame)
        self.ssnLineEdit.setObjectName(u"ssnLineEdit")
        self.ssnLineEdit.setEnabled(True)
        sizePolicy.setHeightForWidth(self.ssnLineEdit.sizePolicy().hasHeightForWidth())
        self.ssnLineEdit.setSizePolicy(sizePolicy)
        self.ssnLineEdit.setMinimumSize(QSize(180, 50))
        self.ssnLineEdit.setMaximumSize(QSize(230, 50))
        font8 = QFont()
        font8.setPointSize(18)
        self.ssnLineEdit.setFont(font8)
        self.ssnLineEdit.setStyleSheet(u"background-color: rgb(255, 255, 127);\n"
"color: rgb(32, 75, 70);")
        self.ssnLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ssnLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ssnLineEdit.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.ssnLineEdit, 2, 0, 1, 1)


        self.gridLayout_9.addWidget(self.lenderInfoFrame, 0, 0, 1, 1)

        self.carInfoFrame = QFrame(self.frame_2)
        self.carInfoFrame.setObjectName(u"carInfoFrame")
        sizePolicy.setHeightForWidth(self.carInfoFrame.sizePolicy().hasHeightForWidth())
        self.carInfoFrame.setSizePolicy(sizePolicy)
        self.carInfoFrame.setMinimumSize(QSize(260, 360))
        self.carInfoFrame.setMaximumSize(QSize(360, 460))
        self.carInfoFrame.setFrameShape(QFrame.Shape.Box)
        self.carInfoFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_11 = QGridLayout(self.carInfoFrame)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.carInfoLabel = QLabel(self.carInfoFrame)
        self.carInfoLabel.setObjectName(u"carInfoLabel")
        sizePolicy.setHeightForWidth(self.carInfoLabel.sizePolicy().hasHeightForWidth())
        self.carInfoLabel.setSizePolicy(sizePolicy)
        self.carInfoLabel.setMinimumSize(QSize(180, 50))
        self.carInfoLabel.setMaximumSize(QSize(230, 50))
        font9 = QFont()
        font9.setPointSize(14)
        self.carInfoLabel.setFont(font9)
        self.carInfoLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.carInfoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.carInfoLabel, 1, 0, 1, 1)

        self.vehiclePictureLabel = QLabel(self.carInfoFrame)
        self.vehiclePictureLabel.setObjectName(u"vehiclePictureLabel")
        sizePolicy.setHeightForWidth(self.vehiclePictureLabel.sizePolicy().hasHeightForWidth())
        self.vehiclePictureLabel.setSizePolicy(sizePolicy)
        self.vehiclePictureLabel.setMinimumSize(QSize(180, 180))
        self.vehiclePictureLabel.setMaximumSize(QSize(210, 210))
        self.vehiclePictureLabel.setPixmap(QPixmap(u"uiPictures/OXZ915.png"))
        self.vehiclePictureLabel.setScaledContents(True)

        self.gridLayout_11.addWidget(self.vehiclePictureLabel, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.carInfoFrame, 0, 3, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 2, 0, 1, 1)

        self.stackedWidget.addWidget(self.lendPage)
        self.returnPage = QWidget()
        self.returnPage.setObjectName(u"returnPage")
        self.gridLayout_6 = QGridLayout(self.returnPage)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.returnCarFrame = QFrame(self.returnPage)
        self.returnCarFrame.setObjectName(u"returnCarFrame")
        sizePolicy2.setHeightForWidth(self.returnCarFrame.sizePolicy().hasHeightForWidth())
        self.returnCarFrame.setSizePolicy(sizePolicy2)
        self.returnCarFrame.setMaximumSize(QSize(300, 300))
        self.returnCarFrame.setFrameShape(QFrame.Shape.Box)
        self.returnCarFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout = QGridLayout(self.returnCarFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.keyPictureReturnLabel = QLabel(self.returnCarFrame)
        self.keyPictureReturnLabel.setObjectName(u"keyPictureReturnLabel")
        self.keyPictureReturnLabel.setEnabled(True)
        self.keyPictureReturnLabel.setMaximumSize(QSize(210, 210))
        self.keyPictureReturnLabel.setPixmap(QPixmap(u":/pictures/uiPictures/keys.png"))
        self.keyPictureReturnLabel.setScaledContents(True)

        self.gridLayout.addWidget(self.keyPictureReturnLabel, 0, 0, 1, 1)

        self.keyReturnBarcodeLineEdit = QLineEdit(self.returnCarFrame)
        self.keyReturnBarcodeLineEdit.setObjectName(u"keyReturnBarcodeLineEdit")
        self.keyReturnBarcodeLineEdit.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.keyReturnBarcodeLineEdit.sizePolicy().hasHeightForWidth())
        self.keyReturnBarcodeLineEdit.setSizePolicy(sizePolicy4)
        self.keyReturnBarcodeLineEdit.setMaximumSize(QSize(180, 50))
        self.keyReturnBarcodeLineEdit.setFont(font7)
        self.keyReturnBarcodeLineEdit.setStyleSheet(u"background-color: rgb(208, 208, 208);")
        self.keyReturnBarcodeLineEdit.setFrame(False)
        self.keyReturnBarcodeLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.keyReturnBarcodeLineEdit.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.keyReturnBarcodeLineEdit, 2, 0, 1, 1)

        self.registerPlateBGReturnLabel = QLabel(self.returnCarFrame)
        self.registerPlateBGReturnLabel.setObjectName(u"registerPlateBGReturnLabel")
        self.registerPlateBGReturnLabel.setMaximumSize(QSize(180, 50))
        self.registerPlateBGReturnLabel.setPixmap(QPixmap(u":/pictures/uiPictures/plateBGPicture.png"))
        self.registerPlateBGReturnLabel.setScaledContents(True)

        self.gridLayout.addWidget(self.registerPlateBGReturnLabel, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.returnCarFrame, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_6, 1, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.returnPage)

        self.verticalLayout_5.addWidget(self.stackedWidget)

        self.bottomFrame = QFrame(self.centralwidget)
        self.bottomFrame.setObjectName(u"bottomFrame")
        self.bottomFrame.setFrameShape(QFrame.Shape.Box)
        self.bottomFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.bottomFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.okPushButton = QPushButton(self.bottomFrame)
        self.okPushButton.setObjectName(u"okPushButton")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.okPushButton.sizePolicy().hasHeightForWidth())
        self.okPushButton.setSizePolicy(sizePolicy5)
        self.okPushButton.setMinimumSize(QSize(250, 55))
        self.okPushButton.setMaximumSize(QSize(250, 55))
        font10 = QFont()
        font10.setPointSize(24)
        font10.setBold(True)
        self.okPushButton.setFont(font10)
        self.okPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.okPushButton.setStyleSheet(u"background-color: rgb(140, 51, 85);\n"
"color: rgb(255, 255, 255);")
        self.okPushButton.setIconSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.okPushButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.goBackPushButton = QPushButton(self.bottomFrame)
        self.goBackPushButton.setObjectName(u"goBackPushButton")
        sizePolicy5.setHeightForWidth(self.goBackPushButton.sizePolicy().hasHeightForWidth())
        self.goBackPushButton.setSizePolicy(sizePolicy5)
        self.goBackPushButton.setMinimumSize(QSize(250, 55))
        self.goBackPushButton.setMaximumSize(QSize(250, 55))
        self.goBackPushButton.setFont(font10)
        self.goBackPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.goBackPushButton.setStyleSheet(u"background-color: rgb(140, 51, 85);\n"
"color: rgb(255, 255, 255);")
        icon2 = QIcon()
        icon2.addFile(u":/pictures/uiPictures/back.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.goBackPushButton.setIcon(icon2)
        self.goBackPushButton.setIconSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.goBackPushButton)


        self.verticalLayout_5.addWidget(self.bottomFrame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1318, 33))
        self.menubar.setStyleSheet(u"background-color: rgb(0, 33, 72);\n"
"color: rgb(255, 255, 255);")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setFont(font)
        self.statusbar.setToolTipDuration(-1)
        self.statusbar.setStyleSheet(u"background-color: rgb(243, 89, 148);")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Rasekon ajoneuvojen lainaus", None))
        self.soundCheckBox.setText("")
        self.logoLabel_3.setText("")
        self.availablePlainTextEdit_2.setPlainText("")
        self.availableLabel_2.setText(QCoreApplication.translate("MainWindow", u"VAPAANA", None))
        self.inUsePlainTextEdit_2.setPlainText(QCoreApplication.translate("MainWindow", u"AM-15 Renault Megane 5 henkil\u00f6\u00e4", None))
        self.inUseLabel_2.setText(QCoreApplication.translate("MainWindow", u"AJOSSA", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Tila", None))
#if QT_CONFIG(tooltip)
        self.takeCarPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Avaa auton lainausikkunan</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.takeCarPushButton.setText(QCoreApplication.translate("MainWindow", u"LAINAA", None))
#if QT_CONFIG(tooltip)
        self.returnCarPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Avaa auton palautusikkunan</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.returnCarPushButton.setText(QCoreApplication.translate("MainWindow", u"PALAUTA", None))
        self.reasonComboBox.setCurrentText("")
        self.reasonComboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ajon tarkoitus", None))
        self.dateLabel.setText("")
        self.calendarLabel.setText("")
        self.timeLabel.setText("")
        self.clockLabel.setText("")
        self.registerPlateBGLabel.setText("")
        self.keyBarcodeLineEdit.setText("")
        self.keyBarcodeLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Lue avain", None))
        self.keyPictureLabel.setText("")
        self.lenderPictureLabel.setText("")
        self.lenderNameLabel.setText(QCoreApplication.translate("MainWindow", u"Lainaajan nimi", None))
        self.ssnLineEdit.setText("")
        self.ssnLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Lue ajokortti", None))
        self.carInfoLabel.setText(QCoreApplication.translate("MainWindow", u"Merkki ja malli", None))
        self.vehiclePictureLabel.setText("")
        self.keyPictureReturnLabel.setText("")
        self.keyReturnBarcodeLineEdit.setText("")
        self.keyReturnBarcodeLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Lue avain", None))
        self.registerPlateBGReturnLabel.setText("")
#if QT_CONFIG(tooltip)
        self.okPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Tallentaa tiedot ajop\u00e4iv\u00e4kirjaan</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.okPushButton.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.goBackPushButton.setText(QCoreApplication.translate("MainWindow", u"KUMOA", None))
    # retranslateUi

