from PyQt5.QtWidgets import QApplication,QDialog,QWidget,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import paramiko
import time
import xmltodict


def errorWindow(self,textToDisplay):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("An Error Occured!")
    msg.setWindowTitle("Error")
    msg.setDetailedText("The details are as follows:\n" + textToDisplay)
    returnValue = msg.exec_()






