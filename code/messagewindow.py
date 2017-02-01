from PyQt5.QtWidgets import *

def messageWindow(textHeader, textToDisplay,isError):
    msg = QMessageBox()
    #Is it just an information popup or an error message (just affects the icon displayed)
    if isError:
        msg.setIcon(QMessageBox.Critical)
    else:
        msg.setIcon(QMessageBox.Information)
    msg.setText(textHeader)
    msg.setWindowTitle("Error")
    msg.setDetailedText(textToDisplay)
    returnValue = msg.exec_()