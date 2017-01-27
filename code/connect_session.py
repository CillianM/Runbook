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


def send_command(term, cmd):
    term.send(cmd + "\n")
    time.sleep(3)
    output = term.recv(2024)
    # Convert byte output to string
    fOutput = output.decode("utf-8")
    # print(fOutput)
    return fOutput

def parse_xml_serial(xml, username):
    try:
        with open(xml) as fd:
            mydict = xmltodict.parse(fd.read())
        serial = "".format(mydict['rpc-reply']['chassis-inventory']['chassis']['serial-number'])
        return True

    except:
        return False

def parse_xml_version(xml, term):
    try:
        with open(xml) as fd:
            mydict = xmltodict.parse(fd.read())
        oldVersion = mydict['rpc-reply']['snapshot-information']['software-version'][0]['package'][
            'package-version']
        newVersion = mydict['rpc-reply']['snapshot-information']['software-version'][1]['package'][
            'package-version']
        if (newVersion == "abc"):
            send_command(term, "show system snapshot media internal")
            if (oldVersion == "abc"):
                send_command(term, "configure")
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def check(term, timeToWait, promptToWaitFor):
    timesChecked = 1
    ready = False
    while (not ready):
        time.sleep(timeToWait)
        answer = send_command(term, "")
        # print(answer)
        if (promptToWaitFor in answer):
            ready = True
        timesChecked = timesChecked + 1

def _login(term):
    send_command(term, "root")
    send_command(term, "")
    send_command(term, "cli")

#Credit to exvito for patch
#link: https://github.com/pyca/cryptography/issues/2039
def patch_crypto_be_discovery():
    """
    Monkey patches cryptography's backend detection.
    Objective: support pyinstaller freezing.
    """
    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
        ]

