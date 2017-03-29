from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ImageButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(ImageButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

class ImageLable(QFrame):
    def __init__(self, icon,text, parent=None):
        super(ImageLable, self).__init__(parent)
        self.frame = QFrame()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.addStretch()
        self.icon = QLabel("")
        self.icon.setPixmap(QPixmap(icon))
        self.layout.addWidget(self.icon)
        self.text = QLabel(text + "         ")
        self.text.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.text)
        self.frame.setLayout(self.layout)

    def getWidget(self):
        return self.frame

    def setStyleSheet(self, styling):
        self.frame.setStyleSheet(styling)

    def setWhatsThis(self, str):
        self.text.setWhatsThis(str)

class IconLineEdit(QFrame):
    def __init__(self, icon,placeholderText,isPassword, parent=None):
        super(IconLineEdit, self).__init__(parent)

        self.frame = QFrame()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.icon = QLabel()
        lineIcon = QPixmap(icon)
        self.icon.setPixmap(lineIcon)
        self.icon.setStyleSheet("background-color: rgb(255,255,255);border: 1px solid white;")
        self.layout.addWidget(self.icon)
        self.lineEdit = QLineEdit()
        if isPassword:
            self.lineEdit.setEchoMode(QLineEdit.Password)
        self.lineEdit.setStyleSheet("background-color: rgb(255,255,255); font-size:16px; border: 1px solid white;")
        self.lineEdit.setPlaceholderText(placeholderText)
        self.layout.addWidget(self.lineEdit)
        self.frame.setStyleSheet("background-color: rgb(255,255,255); border: 1px solid black;")
        self.frame.setLayout(self.layout)

    def getWidget(self):
        return self.frame

    def text(self):
        return self.lineEdit.text()

    def setText(self, text):
        self.lineEdit.setText(text)

    def setWhatsThis(self, str):
        self.lineEdit.setWhatsThis(str)

#top bar layout for everything but the main page
def getTopBarLayout(self,initialWindow): #both the calling window and original window
    topBarLayout = QHBoxLayout()
    topBarLayout.setObjectName("topBarLayout")
    topBarLayout.setSpacing(750)
    backButton = ImageButton(QPixmap("images/back.png"))
    backButton.setObjectName("backButton")
    backButton.clicked.connect(initialWindow.initialiseLauncher)
    topBarLayout.addWidget(backButton)
    refreshButton = ImageButton(QPixmap("images/refresh.png"))
    refreshButton.setObjectName("refreshButton")
    refreshButton.clicked.connect(self.refreshPage)
    refreshButton.setStyleSheet("height: 50px;")
    topBarLayout.addWidget(refreshButton)
    return topBarLayout

def getComboxboxStyle():
    return """

                QComboBox
                {
                    background-color: white;
                    border-radius: 3px;
                    padding: 1px 18px 1px 3px;
                    min-width: 6em;
                }

                QComboBox:editable {
                    background: white;
                }

                QComboBox:!editable, QComboBox::drop-down:editable {
                     background: white
                }

                /* QComboBox gets the "on" state when the popup is open */
                QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                    background: lightgray
                }

                QComboBox::drop-down
                {
                    background-color: white;
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 15px;

                    border-left-width: 1px;
                    border-left-color: darkgray;
                    border-left-style: solid;
                    border-top-right-radius: 3px;
                    border-bottom-right-radius: 3px;
                }

                QComboBox::down-arrow
                {
                    border: 2px solid rgb(0,188,212);
                    width: 3px;
                    height: 3px;
                    background: white;
                }

                QComboBox QAbstractItemView {
                    border: 2px solid darkgray;
                    selection-background-color: lightgray;
                }
            """

def getVerticalScrollStyle():
    return """
                        QScrollBar:vertical {
                             border: 2px solid grey;
                             background: rgb(0,188,212);
                             width: 15px;
                             margin: 22px 0 22px 0;
                        }
                        QScrollBar::handle:vertical {
                             background: white;
                             min-height: 20px;
                        }
                        QScrollBar::add-line:vertical {
                             border: 2px solid grey;
                             background: rgb(0,188,212);
                             height: 20px;
                             subcontrol-position: bottom;
                             subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:vertical {
                             border: 2px solid grey;
                             background: rgb(0,188,212);
                             height: 20px;
                             subcontrol-position: top;
                             subcontrol-origin: margin;
                        }
                        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                             border: 2px solid grey;
                             width: 3px;
                             height: 3px;
                             background: white;
                        }

                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                             background: none;
                        }

                        """

def getHorizontalScrollStyle():
    return """
                        QScrollBar:horizontal {
                            border: 2px solid grey;
                            background: rgb(0,188,212);
                            height: 15px;
                            margin: 0px 20px 0 20px;
                        }
                        QScrollBar::handle:horizontal {
                            background: white;
                            min-width: 20px;
                        }
                        QScrollBar::add-line:horizontal {
                            border: 2px solid grey;
                            background: rgb(0,188,212);
                            width: 20px;
                            subcontrol-position: right;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:horizontal {
                            border: 2px solid grey;
                            background: rgb(0,188,212);
                            width: 20px;
                            subcontrol-position: left;
                            subcontrol-origin: margin;
                        }

                        QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                            border: 2px solid grey;
                            width: 3px;
                            height: 3px;
                            background: white;
                        }

                        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                            background: none;
                        }
                        """