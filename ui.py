# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pomodoro.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QStatusBar, QTimeEdit, QVBoxLayout,
    QWidget)

from gauge_widget import GaugeWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 300)
        MainWindow.setMaximumSize(QSize(500, 400))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_4 = QVBoxLayout(self.page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.timeEdit_2 = QTimeEdit(self.page)
        self.timeEdit_2.setObjectName(u"timeEdit_2")
        self.timeEdit_2.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.timeEdit_2.setStyleSheet(u"QTimeEdit {\n"
"    border: 2px solid #4a62ad;       /* \u0421\u0438\u043d\u044f\u044f \u0440\u0430\u043c\u043a\u0430 */\n"
"    border-radius: 6px;              /* \u0421\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u0443\u0433\u043b\u043e\u0432 */\n"
"    padding: 5px 10px;               /* \u041e\u0442\u0441\u0442\u0443\u043f\u044b \u0432\u043d\u0443\u0442\u0440\u0438 \u043f\u043e\u043b\u044f */\n"
"    background-color: #ffffff;       /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 */\n"
"    color: #333333;                  /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"    font-family: \"Segoe UI\", Arial;  /* \u0428\u0440\u0438\u0444\u0442 */\n"
"    font-size: 16px;                 /* \u0420\u0430\u0437\u043c\u0435\u0440 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* \u0421\u0442\u0438\u043b\u044c \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 \u043c\u044b\u0448\u0438 \u043d\u0430 \u043f\u043e\u043b"
                        "\u0435 */\n"
"QTimeEdit:hover {\n"
"    border: 2px solid #354580;       /* \u0422\u0435\u043c\u043d\u043e-\u0441\u0438\u043d\u044f\u044f \u0440\u0430\u043c\u043a\u0430 */\n"
"}\n"
"\n"
"/* \u0421\u0442\u0438\u043b\u0438\u0437\u0430\u0446\u0438\u044f \u0431\u043b\u043e\u043a\u0430 \u0441 \u043a\u043d\u043e\u043f\u043a\u0430\u043c\u0438 \"\u0432\u0432\u0435\u0440\u0445-\u0432\u043d\u0438\u0437\" */\n"
"QTimeEdit::up-button, QTimeEdit::down-button {\n"
"    subcontrol-origin: border;\n"
"    width: 20px;                     /* \u0428\u0438\u0440\u0438\u043d\u0430 \u043a\u043d\u043e\u043f\u043e\u043a */\n"
"    background: #eaeaea;             /* \u0424\u043e\u043d \u043a\u043d\u043e\u043f\u043e\u043a */\n"
"    border-left: 1px solid #4a62ad;  /* \u0420\u0430\u0437\u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c\u043d\u0430\u044f \u043b\u0438\u043d\u0438\u044f */\n"
"}\n"
"\n"
"/* \u041e\u0442\u0434\u0435\u043b\u044c\u043d\u043e \u0432\u0435\u0440\u0445\u043d\u044f\u044f \u043a\u043d\u043e\u043f\u043a\u0430 */\n"
""
                        "QTimeEdit::up-button {\n"
"    subcontrol-position: top right;  /* \u041f\u043e\u0437\u0438\u0446\u0438\u044f \u0432\u0432\u0435\u0440\u0445\u0443 \u0441\u043f\u0440\u0430\u0432\u0430 */\n"
"    border-top-right-radius: 4px;\n"
"}\n"
"\n"
"/* \u041e\u0442\u0434\u0435\u043b\u044c\u043d\u043e \u043d\u0438\u0436\u043d\u044f\u044f \u043a\u043d\u043e\u043f\u043a\u0430 */\n"
"QTimeEdit::down-button {\n"
"    subcontrol-position: bottom right; /* \u041f\u043e\u0437\u0438\u0446\u0438\u044f \u0432\u043d\u0438\u0437\u0443 \u0441\u043f\u0440\u0430\u0432\u0430 */\n"
"    border-bottom-right-radius: 4px;\n"
"}\n"
"\n"
"/* \u042d\u0444\u0444\u0435\u043a\u0442 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 \u043d\u0430 \u043a\u043d\u043e\u043f\u043a\u0438 */\n"
"QTimeEdit::up-button:pressed, QTimeEdit::down-button:pressed {\n"
"    background: #4a62ad;\n"
"}")
        self.timeEdit_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timeEdit_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.timeEdit_2, 1, 0, 1, 1)

        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 4, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 4, 2, 1, 1)

        self.startCycleButton = QPushButton(self.page)
        self.startCycleButton.setObjectName(u"startCycleButton")

        self.gridLayout.addWidget(self.startCycleButton, 4, 1, 1, 1)

        self.timeEdit = QTimeEdit(self.page)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setStyleSheet(u"QTimeEdit {\n"
"    border: 2px solid #4a62ad;       /* \u0421\u0438\u043d\u044f\u044f \u0440\u0430\u043c\u043a\u0430 */\n"
"    border-radius: 6px;              /* \u0421\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435 \u0443\u0433\u043b\u043e\u0432 */\n"
"    padding: 5px 10px;               /* \u041e\u0442\u0441\u0442\u0443\u043f\u044b \u0432\u043d\u0443\u0442\u0440\u0438 \u043f\u043e\u043b\u044f */\n"
"    background-color: #ffffff;       /* \u0426\u0432\u0435\u0442 \u0444\u043e\u043d\u0430 */\n"
"    color: #333333;                  /* \u0426\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"    font-family: \"Segoe UI\", Arial;  /* \u0428\u0440\u0438\u0444\u0442 */\n"
"    font-size: 16px;                 /* \u0420\u0430\u0437\u043c\u0435\u0440 \u0442\u0435\u043a\u0441\u0442\u0430 */\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* \u0421\u0442\u0438\u043b\u044c \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 \u043c\u044b\u0448\u0438 \u043d\u0430 \u043f\u043e\u043b"
                        "\u0435 */\n"
"QTimeEdit:hover {\n"
"    border: 2px solid #354580;       /* \u0422\u0435\u043c\u043d\u043e-\u0441\u0438\u043d\u044f\u044f \u0440\u0430\u043c\u043a\u0430 */\n"
"}\n"
"\n"
"/* \u0421\u0442\u0438\u043b\u0438\u0437\u0430\u0446\u0438\u044f \u0431\u043b\u043e\u043a\u0430 \u0441 \u043a\u043d\u043e\u043f\u043a\u0430\u043c\u0438 \"\u0432\u0432\u0435\u0440\u0445-\u0432\u043d\u0438\u0437\" */\n"
"QTimeEdit::up-button, QTimeEdit::down-button {\n"
"    subcontrol-origin: border;\n"
"    width: 20px;                     /* \u0428\u0438\u0440\u0438\u043d\u0430 \u043a\u043d\u043e\u043f\u043e\u043a */\n"
"    background: #eaeaea;             /* \u0424\u043e\u043d \u043a\u043d\u043e\u043f\u043e\u043a */\n"
"    border-left: 1px solid #4a62ad;  /* \u0420\u0430\u0437\u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c\u043d\u0430\u044f \u043b\u0438\u043d\u0438\u044f */\n"
"}\n"
"\n"
"/* \u041e\u0442\u0434\u0435\u043b\u044c\u043d\u043e \u0432\u0435\u0440\u0445\u043d\u044f\u044f \u043a\u043d\u043e\u043f\u043a\u0430 */\n"
""
                        "QTimeEdit::up-button {\n"
"    subcontrol-position: top right;  /* \u041f\u043e\u0437\u0438\u0446\u0438\u044f \u0432\u0432\u0435\u0440\u0445\u0443 \u0441\u043f\u0440\u0430\u0432\u0430 */\n"
"    border-top-right-radius: 4px;\n"
"}\n"
"\n"
"/* \u041e\u0442\u0434\u0435\u043b\u044c\u043d\u043e \u043d\u0438\u0436\u043d\u044f\u044f \u043a\u043d\u043e\u043f\u043a\u0430 */\n"
"QTimeEdit::down-button {\n"
"    subcontrol-position: bottom right; /* \u041f\u043e\u0437\u0438\u0446\u0438\u044f \u0432\u043d\u0438\u0437\u0443 \u0441\u043f\u0440\u0430\u0432\u0430 */\n"
"    border-bottom-right-radius: 4px;\n"
"}\n"
"\n"
"/* \u042d\u0444\u0444\u0435\u043a\u0442 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 \u043d\u0430 \u043a\u043d\u043e\u043f\u043a\u0438 */\n"
"QTimeEdit::up-button:pressed, QTimeEdit::down-button:pressed {\n"
"    background: #4a62ad;\n"
"}")
        self.timeEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timeEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.timeEdit, 1, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(self.page)
        self.spinBox.setObjectName(u"spinBox")

        self.verticalLayout.addWidget(self.spinBox)


        self.gridLayout.addLayout(self.verticalLayout, 2, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)

        self.verticalLayout_4.addLayout(self.gridLayout)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_2 = QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.stopCycleButton = QPushButton(self.page_2)
        self.stopCycleButton.setObjectName(u"stopCycleButton")

        self.gridLayout_2.addWidget(self.stopCycleButton, 1, 0, 1, 1)

        self.pauseCycleButton = QPushButton(self.page_2)
        self.pauseCycleButton.setObjectName(u"pauseCycleButton")

        self.gridLayout_2.addWidget(self.pauseCycleButton, 1, 1, 1, 1)

        self.widget = GaugeWidget(self.page_2)
        self.widget.setObjectName(u"widget")
        self.widget.setProperty(u"backgroundColor", QColor(255, 255, 255))
        self.widget.setProperty(u"progressBarColor", QColor(226, 62, 255))
        self.widget.setProperty(u"value", 25)

        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 2)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 500, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"WORK TIME (H:MM)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"REST TIME (H:MM)", None))
        self.startCycleButton.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"NUMBER OF CYCLES", None))
        self.stopCycleButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.pauseCycleButton.setText(QCoreApplication.translate("MainWindow", u"PAUSE", None))
    # retranslateUi

