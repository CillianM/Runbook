import unittest
import sys

from customStyling import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

runner = None

'''
.....
----------------------------------------------------------------------
Ran 5 tests in 4.893s

OK
'''

class CustomStylingTesting(unittest.TestCase):
    global runner
    def test_ImageButton(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Testing Imagebutton")
        self.dialog.setStyleSheet("background-color: rgb(69,90,100);")
        self.dialog.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        mainLayout = QVBoxLayout(self.dialog)

        imageButton = ImageButton(QPixmap("../images/deployment.png"))

        mainLayout.addWidget(imageButton)

        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.dialog.exec_()

    def test_ImageLable(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Testing Imagelabel")
        self.dialog.setStyleSheet("background-color: rgb(69,90,100);")
        self.dialog.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        mainLayout = QVBoxLayout(self.dialog)

        imageLabel = ImageLable("../images/hexagon.png","Label")

        imageLabel.setStyleSheet("""
                                    background-color: rgb(0,188,212);
                                    font-size:16px;
                                    border-top-left-radius: 10px;
                                    border-top-right-radius: 10px;
                                 """)

        imageLabel.setWhatsThis("str")

        mainLayout.addWidget(imageLabel.getWidget())

        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.dialog.exec_()

    def test_IconLineEdit(self):

        self.dialog = QDialog()
        self.dialog.setWindowTitle("Testing Imagelabel")
        self.dialog.setStyleSheet("background-color: rgb(69,90,100);")
        self.dialog.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        mainLayout = QVBoxLayout(self.dialog)

        lineEdit = IconLineEdit("../images/user.png", "Label",False)

        mainLayout.addWidget(lineEdit.getWidget())

        passwordEdit = IconLineEdit("../images/key.png", "Label",True)

        passwordEdit.setText("text")
        print(passwordEdit.text())

        passwordEdit.setWhatsThis("a thing")

        mainLayout.addWidget(passwordEdit.getWidget())

        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.dialog.exec_()

    def test_getTopBarLayout(self):
        topBarLayout = getTopBarLayout(runner,runner)

        self.dialog = QDialog()
        self.dialog.setWindowTitle("Testing topBarLayout")
        self.dialog.setStyleSheet("background-color: rgb(69,90,100);")
        self.dialog.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        mainLayout = QVBoxLayout(self.dialog)
        mainLayout.addLayout(topBarLayout)

        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.dialog.exec_()

    def test_getStylings(self):
        self.assertNotEqual(getComboxboxStyle(),"")
        self.assertNotEqual(getHorizontalScrollStyle(),"")
        self.assertNotEqual(getVerticalScrollStyle(),"")


# class to actually run the QT window
class WindowRunner(QWidget):
    def __init__(self):
        super(WindowRunner,self).__init__()
        global runner
        runner = self
        unittest.main()

    def initialiseLauncher(self):
        print("launcher")

    def refreshPage(self):
        print("refresh")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    runner = WindowRunner()