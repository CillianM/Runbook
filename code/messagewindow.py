from PyQt5.QtWidgets import *

def messageWindow(textHeader, textToDisplay,isError):
    msg = QMessageBox()
    if isError:
        msg.setIcon(QMessageBox.Critical)
    else:
        msg.setIcon(QMessageBox.Information)
    msg.setText(textHeader)
    msg.setWindowTitle("Error")
    msg.setDetailedText("The details are as follows:\n" + textToDisplay)
    returnValue = msg.exec_()