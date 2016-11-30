from PyQt5.QtWidgets import QApplication,QDialog,QWidget,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import paramiko
import time
import xmltodict
import threading

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConnectSession(QtWidgets.QDialog):
    window = ""
    def setupUi(self, ConnectSession):
        self.stages = []
        self.messages = []
        self.index = 0
        window = self
        super(Ui_ConnectSession, self).__init__()
        self.setObjectName("ConnectSession")
        self.setEnabled(True)
        self.setFixedSize(885, 978)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Cillian Mc Neill/Downloads/network.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConnectSession.setWindowIcon(icon)
        self.gridWidget = QtWidgets.QWidget(ConnectSession)
        self.gridWidget.setGeometry(QtCore.QRect(0, 20, 861, 931))
        self.gridWidget.setObjectName("gridWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.nameLabel = QtWidgets.QLabel(self.gridWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.passwordLabel = QtWidgets.QLabel(self.gridWidget)
        self.passwordLabel.setObjectName("passwordLabel")
        self.gridLayout.addWidget(self.passwordLabel, 2, 0, 1, 1)

        self.deviceLabel = QtWidgets.QLabel(self.gridWidget)
        self.deviceLabel.setObjectName("deviceLabel")
        self.gridLayout.addWidget(self.deviceLabel, 4, 0, 1, 1)

        self.devices = QtWidgets.QComboBox(self.gridWidget)
        self.devices.setObjectName("devices")
        self.gridLayout.addWidget(self.devices, 4, 2, 1, 1)
        self.devices.activated.connect(self.callUpdateUI)

        self.label_2 = QtWidgets.QLabel(self.gridWidget)
        self.label_2.setEnabled(False)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 2, 1, 1)
        self.loginButton = QtWidgets.QPushButton('Login', self)
        self.loginButton.setObjectName("loginButton")
        self.gridLayout.addWidget(self.loginButton, 3, 2, 1, 1)

        self.loginButton.clicked.connect(self._login_btn_clicked)
        self.passwordField = QtWidgets.QLineEdit(self.gridWidget)
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordField.setObjectName("passwordField")
        self.gridLayout.addWidget(self.passwordField, 2, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridWidget)
        self.label_3.setEnabled(False)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 7, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridWidget)
        self.label_4.setEnabled(False)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 8, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridWidget)
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 2, 1, 1)
        self.addressLabel = QtWidgets.QLabel(self.gridWidget)
        self.addressLabel.setObjectName("addressLabel")
        self.gridLayout.addWidget(self.addressLabel, 1, 0, 1, 1)
        self.nameField = QtWidgets.QLineEdit(self.gridWidget)
        self.nameField.setObjectName("nameField")
        self.gridLayout.addWidget(self.nameField, 0, 2, 1, 1)
        self.addressField = QtWidgets.QLineEdit(self.gridWidget)
        self.addressField.setObjectName("addressField")
        self.gridLayout.addWidget(self.addressField, 1, 2, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.gridWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 10, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridWidget)
        self.label_5.setEnabled(False)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 9, 2, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(ConnectSession)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ConnectSession", "Connnect Session"))
        self.nameLabel.setText(_translate("ConnectSession", "Username"))
        self.passwordLabel.setText(_translate("ConnectSession", "Password"))
        self.label_2.setText(_translate("ConnectSession", "Serial Number Check"))
        self.loginButton.setText(_translate("ConnectSession", "Login"))
        self.label_3.setText(_translate("ConnectSession", "System Software Request"))
        self.label_4.setText(_translate("ConnectSession", "Partitioning"))
        self.label.setText(_translate("ConnectSession", "Connected"))
        self.addressLabel.setText(_translate("ConnectSession", "Address"))
        self.label_5.setText(_translate("ConnectSession", "Junos Version Check"))

    def callUpdateUI(self):
        self.updateUI(self.devices.currentText())

    def updateUI(self, name):
        for i in range(len(self.stages)):
            if name in self.stages[i]:
                currentStage = self.stages[i]
                currentStage = currentStage[-1:]
                if (currentStage == "1"):
                    self.updateLabels(True, False, False, False, False)
                elif (currentStage == "2"):
                    self.updateLabels(True, True, False, False, False)
                elif (currentStage == "3"):
                    self.updateLabels(True, True, True, False, False)
                elif (currentStage == "4"):
                    self.updateLabels(True, True, True, True, False)
                elif (currentStage == "5"):
                    self.updateLabels(True, True, True, True, True)
                self.textBrowser.clear()
                self.textBrowser.append(self.messages[i])
                break

    def updateLabels(self, b1, b2, b3, b4, b5):
        self.label.setEnabled(b1)
        self.label_2.setEnabled(b2)
        self.label_3.setEnabled(b3)
        self.label_4.setEnabled(b4)
        self.label_5.setEnabled(b5)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate("ConnectSession", "Connnect Session"))
        self.nameLabel.setText(_translate("ConnectSession", "Username"))
        self.passwordLabel.setText(_translate("ConnectSession", "Password"))
        self.deviceLabel.setText(_translate("ConnectSession", "Device"))
        self.label_2.setText(_translate("ConnectSession", "Serial Number Check"))
        self.loginButton.setText(_translate("ConnectSession", "Login"))
        self.label_3.setText(_translate("ConnectSession", "System Software Request"))
        self.label_4.setText(_translate("ConnectSession", "Partitioning"))
        self.label.setText(_translate("ConnectSession", "Connected"))
        self.addressLabel.setText(_translate("ConnectSession", "Address"))
        self.label_5.setText(_translate("ConnectSession", "Junos Version Check"))

    def _login_btn_clicked(self):
        if len(self.nameField.text()) < 1 or len(self.addressField.text()) < 1:
            QMessageBox.information(self, "Empty Fields", "Please enter a full name and address.")
        else:
            patch_crypto_be_discovery()
            self.devices.addItem(self.nameField.text())
            self.textBrowser.clear()
            self.textBrowser.append("Connection Established You can now add another device")
            self.stages.append(self.nameField.text() + " 1")
            self.messages.append("")
            t = threading.Thread(target=_connect_session, args=(
            self.nameField.text(), self.addressField.text(), self.passwordField.text(), self, self.index))
            t.daemon = True
            t.start()

            self.index += 1

    def updateText(window,textToDisplay,index):
        window.textBrowser.append(textToDisplay)
        window.messages[index] = window.messages[index] + textToDisplay

    def updateProgress(window,specifiedLabel,bool):
        specifiedLabel.setEnabled(bool)


def _connect_session(username, hostname, password, window, index):
    try:
        window.updateProgress(window.label,True)
        # replace port colon with underscore for filename
        filename = username.replace(":", "_") + ".xml"
        window.updateText("Filename will be " + filename + "\n",index)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, 22, username, password)
        term = ssh.invoke_shell()
        window.updateText(username + ": " + "Connected\n", index)
        check(term, 5, "login", username, window, index)
        _login(term)
        window.updateText(username + ": " + "Logged in\n", index)
        send_command(term, "set cli screen-length 0")
        window.stages[index] = username + " 2"
        window.updateProgress(window.label_2, True)
        xml = send_command(term, "show chassis hardware | display xml")
        xml = xml[37:(len(xml)) - 10]
        text_file = open(filename, "w")
        text_file.write(xml)
        text_file.close()
        window.updateText(username + ": " + "Parsing xml for serial\n",index)
        parse_xml_serial(filename, username, window, index)
        window.stages[index] = username + " 3"
        window.updateProgress(window.label_3, True)
        send_command(term,
                     "request system software add \"ftp://10.179.236.10/junos-srxsme-15.1X49-D60.7-domestic.tgz\" no-copy no-validate reboot")
        window.updateText(username + ": " + "Requested System software, waiting 2 minutes looped\n", index)
        check(term, 120, "login", username, window, index)
        _login(term)
        window.updateText(username + ": " + "Logged in again\n",index)
        window.stages[index] = username + " 4"
        window.updateProgress(window.label_4, True)
        send_command(term, "request system snapshot media internal slice alternate")
        window.updateText(username + ": " + "Requested system snapshot, waiting 1 minute looped\n",index)
        check(term, 60, "root", username, window, index)
        window.updateText(username + ": " + "Request accepted, Partitioned snapshot\n", index)
        send_command(term, "set cli screen-length 0")
        window.updateText(username + ": " + "Seraching Junos version\n", index)
        window.stages[index] = username + " 5"
        window.updateProgress(window.label_5, True)
        output = send_command(term, "show system snapshot media internal | display xml")
        output = output[51:(len(output)) - 10]
        text_file = open(filename, "w")
        text_file.write(output)
        text_file.close()
        window.updateText(username + ": " + "Parsing Junos version\n", index)
        if (parse_xml_version(filename, term, username, window, index)):
            # send_command(term, "delete /yes")
            # send_command(term, "load set \"ftp://Administrator@10.179.236.10/config.conf\"")
            # send_command(term,"set system login user Agile class super-user")
            # send_command(term,"set system login user authentication plain-text-password")
            # send_command(term, "password")
            # send_command(term, "password")
            # send_command(term, "commit-and quit")
            window.updateText(username + ": " + "Versions ok\n", index)
            #window.textBrowser.append(username + ": " + "Versions ok\n")
            send_command(term, "request system halt in 0")
            time.sleep(2)
            send_command(term, "yes")
        else:
            window.updateText(username + ": " + "Versions not configured properly\n", index)

        window.updateText(username + ": " + "Shutting down\n", index)
        send_command(term, "request system halt in 0")
        time.sleep(2)
        send_command(term, "yes")
        ssh.close()
    except paramiko.ssh_exception.BadHostKeyException:
        window.updateText("Host Key Error! Server’s host key could not be verified", index)
    except paramiko.ssh_exception.AuthenticationException:
        window.updateText("Authentication Error! Authentication failed, Check your details and try again", index)
    except paramiko.ssh_exception.SSHException:
        window.updateText("Unknown Error! Unknown error connecting or establishing an SSH session", index)

def updateUI(devicename):
    print(devicename)

def send_command(term, cmd):
    term.send(cmd + "\n")
    time.sleep(3)
    output = term.recv(2024)
    # Convert byte output to string
    fOutput = output.decode("utf-8")
    # print(fOutput)
    return fOutput

def parse_xml_serial(xml, username, window, index):
    try:
        with open(xml) as fd:
            mydict = xmltodict.parse(fd.read())
        window.textBrowser.append(username + ": " + "Serial number is: {}".format(
            mydict['rpc-reply']['chassis-inventory']['chassis']['serial-number']
        ) + "\n")

        window.messages[index] = window.messages[index] + username + ": " + "Serial number is: {}".format(
            mydict['rpc-reply']['chassis-inventory']['chassis']['serial-number']
        ) + "\n"
    except:
        window.textBrowser.append("XML Parse Error\n")
        window.messages[index] = window.messages[index] + "XML Parse Error\n"

def parse_xml_version(xml, term, username, window, index):
    try:
        with open(xml) as fd:
            mydict = xmltodict.parse(fd.read())
        oldVersion = mydict['rpc-reply']['snapshot-information']['software-version'][0]['package'][
            'package-version']
        newVersion = mydict['rpc-reply']['snapshot-information']['software-version'][1]['package'][
            'package-version']
        window.textBrowser.append(username + ": " + "New Version: " + newVersion + "\n")
        window.messages[index] = window.messages[index] + "New Version: " + newVersion + "\n"
        window.textBrowser.append(username + ": " + "Old Version " + oldVersion + "\n")
        window.messages[index] = window.messages[index] + "Old Version " + oldVersion + "\n"
        if (newVersion == "abc"):
            window.textBrowser.append(username + ": " + "New Version updated\n")
            window.messages[index] = window.messages[index] + username + ": " + "New Version updated\n"
            send_command(term, "show system snapshot media internal")
            if (oldVersion == "abc"):
                window.textBrowser.append(username + ": " + "New Version updated\n")
                window.messages[index] = window.messages[index] + username + ": " + "New Version updated\n"
                send_command(term, "configure")
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def check(term, timeToWait, promptToWaitFor, username, window, index):
    timesChecked = 1
    ready = False
    while (not ready):
        time.sleep(timeToWait)
        window.textBrowser.append(
            username + ": " + "Checked " + str(timesChecked) + " Times(s), Looping for another " + str(
                timeToWait) + " seconds waiting for " + promptToWaitFor + "\n")
        window.messages[index] = window.messages[index] + username + ": " + "Checked " + str(
            timesChecked) + " Times(s), Looping for another " + str(
            timeToWait) + " seconds waiting for " + promptToWaitFor + "\n"
        answer = send_command(term, "")
        # print(answer)
        if (promptToWaitFor in answer):
            ready = True
        timesChecked = timesChecked + 1

def _login(term):
    send_command(term, "root")
    send_command(term, "")
    send_command(term, "cli")

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

