import datetime

import pyodbc
from ftplib import FTP

import paramiko
import xmltodict

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time

from imagebutton import ImageButton
import messagewindow as msg

#global variable to save window state
deploymentWindow = None

class DeploymentModule:
    def __init__(self, window, layout):
        self.layout = layout
        self.window = window
        self.blocked = False
        self.threads = []
        global deploymentWindow
        deploymentWindow = self


    def deploymentUI(self, window):
        try:
            self.consolePasswordField = QLineEdit()
            self.fromPortNo = QLineEdit()
            self.toPortNo = QLineEdit()
            self.willCloneToBackup = QCheckBox("Clone to Backup Partition")
            self.dbPasswordField = QLineEdit()
            self.osVersions = QComboBox()
            self.fromConfiguration = QComboBox()
            self.toConfiguration = QComboBox()
            verticalContainer = QVBoxLayout(window)
            verticalContainer.setObjectName("verticalContainer")

            topBarLayout = QHBoxLayout()
            topBarLayout.setObjectName("topBarLayout")
            topBarLayout.setSpacing(750)

            backButton = ImageButton(QPixmap("back.png"))
            backButton.setObjectName("backButton")
            backButton.clicked.connect(window.initialiseLauncher)
            topBarLayout.addWidget(backButton)
            refreshButton = ImageButton(QPixmap("refresh.png"))
            refreshButton.setObjectName("refreshButton")
            refreshButton.clicked.connect(self.refreshPage)
            refreshButton.setStyleSheet("height: 50px;")
            topBarLayout.addWidget(refreshButton)

            verticalContainer.addLayout(topBarLayout)

            innerContainer = QHBoxLayout()
            innerContainer.setContentsMargins(0, 0, 0, 0)
            innerContainer.setObjectName("innerContainer")

            loginFrame = QFrame()
            loginDetailsLayout = QGridLayout()
            loginDetailsLayout.setObjectName("loginDetailsLayout")
            loginDetailsLayout.setVerticalSpacing(30)
            portNoLayout = QGridLayout()
            portNoLayout.setObjectName("portNoLayout")
            label = QLabel("   TO   ")
            label.setObjectName("label")
            label.setStyleSheet("color:white; font-size:16px; border: 1px solid rgb(96,125,139);")
            portNoLayout.addWidget(label, 0, 1, 1, 1)

            self.fromPortNo.setObjectName("fromPortNo")
            self.fromPortNo.setStyleSheet("background-color: rgb(255,255,255);")
            self.fromPortNo.setPlaceholderText("> Port")
            portNoLayout.addWidget(self.fromPortNo, 0, 0, 1, 1)

            self.toPortNo.setObjectName("toPortNo")
            self.toPortNo.setStyleSheet("background-color: rgb(255,255,255);")
            self.toPortNo.setPlaceholderText(">> Port")
            portNoLayout.addWidget(self.toPortNo, 0, 2, 1, 1)
            loginDetailsLayout.addLayout(portNoLayout, 1, 0, 1, 1)
            checkboxLayout = QVBoxLayout()
            checkboxLayout.setObjectName("checkboxLayout")


            self.willCloneToBackup.setObjectName("self.willCloneToBackup")
            self.willCloneToBackup.setStyleSheet("color:white; font-size:16px; border: 1px solid rgb(96,125,139);")
            checkboxLayout.addWidget(self.willCloneToBackup)
            loginDetailsLayout.addLayout(checkboxLayout, 4, 0, 1, 1)

            deploymentButton = QPushButton("Begin Deployment")
            deploymentButton.setObjectName("deploymentButton")
            deploymentButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
            deploymentButton.clicked.connect(startDeployment)
            loginDetailsLayout.addWidget(deploymentButton, 6, 0, 1, 1)

            self.consolePasswordField.setPlaceholderText("Console Server Password")
            self.consolePasswordField.setEchoMode(QLineEdit.Password)
            self.consolePasswordField.setStyleSheet("background-color: rgb(255,255,255);")
            self.consolePasswordField.setObjectName("consolePasswordField")
            loginDetailsLayout.addWidget(self.consolePasswordField, 2, 0, 1, 1)


            self.dbPasswordField.setPlaceholderText("Database Server Password")
            self.dbPasswordField.setEchoMode(QLineEdit.Password)
            self.dbPasswordField.setStyleSheet("background-color: rgb(255,255,255);")
            self.dbPasswordField.setObjectName("dbPasswordField")
            loginDetailsLayout.addWidget(self.dbPasswordField, 3, 0, 1, 1)


            self.osVersions.setObjectName("self.osVersions")
            self.osVersions.setStyleSheet("background-color: rgb(255,255,255);")

            # Connect to ftp and get files for updating os
            self.osVersions.clear()
            thread = FileGrabber(self.window)
            thread.setup(self, ".tgz")
            thread.trigger.connect(self.fillComboBox)
            thread.start()
            self.threads.append(thread)

            loginDetailsLayout.addWidget(self.osVersions, 0, 0, 1, 1)

            configurationRangeFrame = QFrame()
            configurationRangeFrame.setContentsMargins(10, 1, 10, 1)
            configurationRangeLayout = QVBoxLayout()
            configurationRangeLayout.setObjectName("configurationRangeLayout")
            configurationRangeLayout.setSpacing(10)
            configurationRangeHeading = QLabel("Inital Configuration Range(Optional)")
            configurationRangeHeading.setObjectName("configurationRangeHeading")
            configurationRangeHeading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
            configurationRangeLayout.addWidget(configurationRangeHeading)


            self.fromConfiguration.setObjectName("fromConfiguration")
            self.fromConfiguration.setStyleSheet("background-color: rgb(255,255,255);")

            self.toConfiguration.setObjectName("toConfiguration")
            self.toConfiguration.setStyleSheet("background-color: rgb(255,255,255);")

            # connect to ftp and get any files from ftp
            self.fromConfiguration.clear()
            self.toConfiguration.clear()
            thread = FileGrabber(self.window)
            thread.setup(self, ".conf")
            thread.trigger.connect(self.fillComboBox)
            thread.start()
            self.threads.append(thread)

            configurationRangeLayout.addWidget(self.fromConfiguration)
            configurationRangeLayout.addWidget(self.toConfiguration)
            configurationRangeFrame.setLayout(configurationRangeLayout)
            configurationRangeFrame.setStyleSheet("background-color: white; border: 1px solid black; font-size:16px; ")
            loginDetailsLayout.addWidget(configurationRangeFrame, 5, 0, 1, 1)
            loginDetailsLayout.setAlignment(Qt.AlignCenter)

            loginFrame.setLayout(loginDetailsLayout)
            loginFrame.setStyleSheet("background-color: rgb(96,125,139); border: 1px solid black; font-size:16px; ")
            loginEffect = QGraphicsDropShadowEffect()
            loginEffect.setBlurRadius(15)
            loginFrame.setGraphicsEffect(loginEffect)
            innerContainer.addWidget(loginFrame)

            progressBarLayout = QGridLayout()
            progressBarLayout.setObjectName("progressBarLayout")

            self.progressBar = QProgressBar()
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
            self.progressBar.setSizePolicy(sizePolicy)
            self.progressBar.setProperty("value", 0)
            self.progressBar.setOrientation(Qt.Vertical)
            self.progressBar.setInvertedAppearance(True)
            self.progressBar.setTextVisible(False)
            self.progressBar.setTextDirection(QProgressBar.TopToBottom)
            self.progressBar.setObjectName("self.progressBar")
            self.progressBar.setStyleSheet("QProgressBar::chunk:vertical { background-color: rgb(0,188,212);}")

            progressBarLayout.addWidget(self.progressBar, 0, 0, 1, 1)

            progressBarLayout.setContentsMargins(50, 0, 50, 0)
            innerContainer.addLayout(progressBarLayout)

            progressTextFrame = QFrame()
            progressTextLayout = QGridLayout()

            progressTextLayout.setObjectName("progressTextLayout")
            deploymentProgressHeader = QLabel("Deployment Progress")
            deploymentProgressHeader.setObjectName("deploymentProgressHeader")
            deploymentProgressHeader.setStyleSheet("background-color: rgb(0,188,212); border: 1px solid black; font-size:16px;")
            progressTextLayout.addWidget(deploymentProgressHeader, 1, 0, 1, 1)

            self.connectedToDevice = QLabel("Connect to the device")
            self.connectedToDevice.setObjectName("self.connectedToDevice")
            self.connectedToDevice.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
            progressTextLayout.addWidget(self.connectedToDevice, 2, 0, 1, 1)

            self.loggedIn = QLabel("Log in")
            self.loggedIn.setObjectName("self.loggedIn")
            self.loggedIn.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
            progressTextLayout.addWidget(self.loggedIn, 3, 0, 1, 1)

            self.downloadingOS = QLabel("Downloading OS")
            self.downloadingOS.setObjectName("self.downloadingOS")
            self.downloadingOS.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
            progressTextLayout.addWidget(self.downloadingOS, 4, 0, 1, 1)

            self.installingOS = QLabel("Installing OS")
            self.installingOS.setObjectName("self.installingOS")
            self.installingOS.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
            progressTextLayout.addWidget(self.installingOS, 5, 0, 1, 1)

            self.rebootingDevice = QLabel("Rebooting the device")
            self.rebootingDevice.setObjectName("self.rebootingDevice")
            self.rebootingDevice.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
            progressTextLayout.addWidget(self.rebootingDevice, 6, 0, 1, 1)

            self.loggedInAgain = QLabel("Logging into the device")
            self.loggedInAgain.setObjectName("self.loggedInAgain")
            self.loggedInAgain.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
            progressTextLayout.addWidget(self.loggedInAgain, 7, 0, 1, 1)

            self.applyingConfig = QLabel("Applying the configuration file")
            self.applyingConfig.setObjectName("self.applyingConfig")
            self.applyingConfig.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
            progressTextLayout.addWidget(self.applyingConfig, 8, 0, 1, 1)

            self.rebootingTheDeviceAgain = QLabel("Rebooting the device")
            self.rebootingTheDeviceAgain.setObjectName("self.rebootingTheDeviceAgain")
            self.rebootingTheDeviceAgain.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
            progressTextLayout.addWidget(self.rebootingTheDeviceAgain, 9, 0, 1, 1)

            self.deploymentSuccessful = QLabel("Deployment Successful")
            self.deploymentSuccessful.setObjectName("self.deploymentSuccessful")
            self.deploymentSuccessful.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
            progressTextLayout.addWidget(self.deploymentSuccessful, 10, 0, 1, 1)

            progressTextFrame.setLayout(progressTextLayout)
            progressTextFrame.setStyleSheet("background-color: rgb(96,125,139); border: 1px solid black; font-size:16px; ")
            progressTextEffect = QGraphicsDropShadowEffect()
            progressTextEffect.setBlurRadius(15)
            progressTextFrame.setGraphicsEffect(progressTextEffect)
            innerContainer.addWidget(progressTextFrame)
            verticalContainer.addLayout(innerContainer)

            self.layout.setLayout(verticalContainer)
        except Exception as e: print(str(e))

    def clearProgressText(self):
        self.connectedToDevice.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
        self.loggedIn.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
        self.downloadingOS.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
        self.installingOS.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
        self.rebootingDevice.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
        self.loggedInAgain.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
        self.applyingConfig.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
        self.rebootingTheDeviceAgain.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")
        self.deploymentSuccessful.setStyleSheet("color:white; font-size:16px;border: 1px solid rgb(96,125,139);")

    def updateProgress(self, percentage):
        self.progressBar.setValue(percentage)
        if (percentage == 11):
            self.connectedToDevice.setStyleSheet("color:white; font-size:16px;")
        elif (percentage == 22):
            self.loggedIn.setStyleSheet("color:white; font-size:16px;")
        elif (percentage == 44):
            self.downloadingOS.setStyleSheet("color:white; font-size:16px;")
            self.installingOS.setStyleSheet("color:white; font-size:16px;")
        elif (percentage == 55):
            self.rebootingDevice.setStyleSheet("color:white; font-size:16px;")
        elif (percentage == 66):
            self.loggedInAgain.setStyleSheet("color:white; font-size:16px;")
        elif (percentage == 77):
            self.applyingConfig.setStyleSheet("color:white; font-size:16px;")
        elif (percentage == 88):
            self.rebootingTheDeviceAgain.setStyleSheet("color:white; font-size:16px;")
        else:
            self.deploymentSuccessful.setStyleSheet("color:white; font-size:16px;")

    #fill appropriate combo box when code from thread is returned
    def fillComboBox(self,code):
        #deal with conf or tgz depending on code
        if code == 0:
            for index in range(len(self.confFiles)):
                self.fromConfiguration.addItem(self.confFiles[index])
                self.toConfiguration.addItem(self.confFiles[index])
        elif code == 1:
            for index in range(len(self.osFiles)):
                deploymentWindow.osVersions.addItem(self.osFiles[index])


    def refreshPage(self):
        try:
            if (self.blocked):
                msg.messageWindow("Process is currently running", "Cannot refresh page when units are being updated",
                                  False)
            else:
                self.threads.clear()
                self.clearProgressText()
                self.fromConfiguration.clear()
                self.toConfiguration.clear()
                thread = FileGrabber(self.window)
                thread.setup(self,".conf")
                thread.trigger.connect(self.fillComboBox)
                thread.start()
                self.threads.append(thread)

                self.osVersions.clear()
                thread = FileGrabber(self.window)
                thread.setup(self, ".tgz")
                thread.trigger.connect(self.fillComboBox)
                thread.start()
                self.threads.append(thread)

                self.dbPasswordField.setText("")
                self.consolePasswordField.setText("")
                self.willCloneToBackup.setChecked(False)
                self.toPortNo.setText("")
                self.fromPortNo.setText("")
        except Exception as e:
            msg.messageWindow("Error Refreshing","An error occured clearing page and connecting to FTP server, try again later",True)

#File grabber class to get files off UI thread
class FileGrabber(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(FileGrabber, self).__init__(parent)

    def setup(self, deploymentWindow,extension):
        self.deploymentWindow = deploymentWindow
        self.extension = extension

    def run(self):
        if  "conf" in self.extension:
            deploymentWindow.confFiles = getFiles(self.extension)
            self.trigger.emit(0)
        else:
            deploymentWindow.osFiles = getFiles(self.extension)
            self.trigger.emit(1)


#launch the beginDeployment method through this in the .connect of the ui
def startDeployment(self):
    global deploymentWindow
    beginDeployment(deploymentWindow)

def beginDeployment(deploymentWindow):
    try:
        deploymentWindow.threads.clear()
        # Make sure fields aren't empty
        if fieldsEmpty(deploymentWindow):
            msg.messageWindow("Empty Fields", "Please ensure all the fields are filled",True)
            return
        # Make sure both port numbers are actually numbers
        if (not isNumber(deploymentWindow.toPortNo.text()) or not isNumber(deploymentWindow.fromPortNo.text())):
            msg.messageWindow("Not a Number", "Please ensure ports are numbers",True)
            return

        # make sure configurations are the same amount as devices being updated
        fromConf = deploymentWindow.fromConfiguration.currentIndex()
        toConf = deploymentWindow.toConfiguration.currentIndex()
        fromPort = int(deploymentWindow.fromPortNo.text())
        toPort = int(deploymentWindow.toPortNo.text())
        if (not (toConf >= fromConf)):
            msg.messageWindow("Config List Error","Please ensure your starting configuration is before your final configuration", True)
            return
        if (not ((toConf - fromConf) + 1 == (toPort - fromPort) + 1)):
            msg.messageWindow("Not Enough Configs","Please ensure there are enough config files for each specified device",True)
            return

        # apply patch
        patch_crypto_be_discovery()
        configurationsToUse = []
        for index in range(fromConf, toConf + 1):
            configurationsToUse.append(deploymentWindow.confFiles[index])

        willBackup = deploymentWindow.willCloneToBackup.isChecked()
        OsFile = deploymentWindow.osVersions.currentText()
        consolePassword = deploymentWindow.consolePasswordField.text()
        databasePassword = deploymentWindow.dbPasswordField.text()
        deploymentWindow.progressBar.setValue(0)

        confIndex = fromConf
        # check to see how many devices we're updating
        if (toPort - fromPort + 1 == 1):
            thread = Updater(deploymentWindow.window)
            thread.trigger.connect(deploymentWindow.updateProgress)
            thread.setup(toPort, consolePassword, databasePassword, OsFile, configurationsToUse[confIndex], willBackup,
                         True)
            thread.start()
            deploymentWindow.threads.append(thread)

        else:
            confIndex = 0
            for index in range(fromPort, toPort):
                thread = Updater(deploymentWindow.window)
                thread.trigger.connect(deploymentWindow.updateProgress)
                thread.setup(index, consolePassword, databasePassword, OsFile, configurationsToUse[confIndex],
                             willBackup,
                             False)
                thread.start()
                deploymentWindow.threads.append(thread)
                confIndex += 1

            # make final thread the one to update GUI
            thread.trigger.connect(deploymentWindow.updateProgress)
            thread.setup(toPort, consolePassword, databasePassword, OsFile, configurationsToUse[confIndex], willBackup,
                         True)
            thread.start()
            deploymentWindow.threads.append(thread)
    except Exception as e:
        print(str(e))


def fieldsEmpty(deploymentWindow):
    if (len(deploymentWindow.fromPortNo.text()) < 1 or len(deploymentWindow.toPortNo.text()) < 1 or len(deploymentWindow.consolePasswordField.text()) < 1):
        return True
    else:
        return False

def getFiles(extension):
    try:
        # anonymous login so no password
        if ("conf" in extension):
            # set the ftp path to the config files location
            path = getIniConfPath()
        else:
            # set the ftp path to the os files location
            path = getOsPath()
        address = getFtpAddress()
        # don't need to specifiy port in localhost
        if 'localhost' in address:
            ftp = FTP(address)
        else:
            ftp = FTP(address, '21')
        ftp.login('anonymous', '')
        ftp.cwd(path)

        # get list of all the files in the directory
        files = ftp.nlst()
        actualFiles = []
        # add all the files with the appropriate extension to the list
        for index in range(len(files)):
            if (extension in files[index]):
                actualFiles.append(files[index])
        actualFiles.reverse()
        return actualFiles

    except:
        return []


def isNumber(number):
    try:
        int(number)
    except ValueError:
        return False
    else:
        return True


class Updater(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Updater, self).__init__(parent)

    def setup(self, thread_no,consolePassword,databsePassword,OsFile,configFile,willClone,isGUIUpdater):
        self.thread_no = thread_no
        self.databsePassword = databsePassword
        self.consolePassword = consolePassword
        self.willClone = willClone
        self.configFile = configFile
        self.isGUIUpdater = isGUIUpdater
        self.OsFile = OsFile

    def run(self):
        self.connect_session(self.thread_no,self.consolePassword,self.databsePassword,self.OsFile,self.configFile,self.willClone,self.isGUIUpdater)


    def connect_session(self,portNo, consolePassword,databasePassword,OsFile,configFile,willClone,updateGui):
        try:
            # replace port colon with underscore for filename
            ftpAddress = getFtpAddress()
            osFile = getOsPath() + OsFile
            confPath = getIniConfPath() + configFile
            username = getConsoleName()
            hostname = username + ":" + str(portNo) + "@" + getConsoleAddress()
            filename = username + ":" + str(portNo) + ".xml"

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, 22, username, consolePassword)
            term = ssh.invoke_shell()
            if(updateGui):
                self.trigger.emit(11)
            check(term, 5, "login")
            _login(term)
            if (updateGui):
                self.trigger.emit(22)
            send_command(term, "set cli screen-length 0")
            originalVersion = send_command(term, "show system version")


            xml = send_command(term, "show chassis hardware | display xml")
            xml = xml[37:(len(xml)) - 10]
            text_file = open(filename, "w")
            text_file.write(xml)
            text_file.close()
            # parsing for serial
            serialNo = parse_xml_serial(filename, username)
            #push serial to database
            pushSerial(getDatabaseAddress(),getDatabaseUsername(),databasePassword,serialNo,confPath)

            if (updateGui):
                self.trigger.emit(44)
            send_command(term,"request system software add \"" + ftpAddress + "\\" + osFile + "\" no-copy no-validate reboot")

            if (updateGui):
                self.trigger.emit(55)
            check(term, 120, "login")
            _login(term)

            if (updateGui):
                self.trigger.emit(66)
            if(willClone):
                send_command(term, "request system snapshot media internal slice alternate")
            # requested system snapshot
            check(term, 60, "root")
            # partitioned snapshot
            send_command(term, "set cli screen-length 0")
            # junos version check
            output = send_command(term, "show system snapshot media internal | display xml")
            output = output[51:(len(output)) - 10]
            text_file = open(filename, "w")
            text_file.write(output)
            text_file.close()
            updatedVersion = send_command(term, "show system version")
            if (updateGui):
                self.trigger.emit(77)
            if not updatedVersion == originalVersion:
                send_command(term, "configure")
                send_command(term, "delete /yes")
                send_command(term, "load set \""+ ftpAddress  + "\"" + confPath)
                send_command(term, "commit-and-quit")
                send_command(term, "request system halt in 0")
                time.sleep(2)
                send_command(term, "yes")
            else:
                QMessageBox.information(self, "Error updating SerialNo: " + serialNo, "OS wasn't updated correctly, Not applying config, Shutting down")

            if (updateGui):
                self.trigger.emit(88)
            send_command(term, "request system halt in 0")
            time.sleep(2)
            send_command(term, "yes")
            ssh.close()
            if (updateGui):
                self.trigger.emit(100)
        except paramiko.ssh_exception.BadHostKeyException:
            msg.messageWindow("Host Key Error!", "Server’s host key could not be verified",True)
        except paramiko.ssh_exception.AuthenticationException:
            msg.messageWindow("Authentication Error!","Authentication failed, Check your details and try again",True)
        except paramiko.ssh_exception.SSHException:
            msg.messageWindow("Unknown Error!", "Unknown error connecting or establishing an SSH session",True)

# Credit to exvito for patch
# link: https://github.com/pyca/cryptography/issues/2039
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

def pushSerial(dbAddress, dbUsername, dbPassword, serialNo, configFile):
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + dbAddress + ';DATABASE=runbook;UID=' + dbUsername + ';PWD=' + dbPassword)
    cursor = cnxn.cursor()
    time = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M %d-%m-%y')
    configTable = getDatabaseConfTable()
    cursor.execute(
        "insert into configTable(serial,user,path,timestamp,isprimary) values (serialNo,dbUsername,configFile,time,1)")
    cnxn.commit()

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
        return serial

    except:
        return ""

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

def getFtpAddress():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Ftp-Info']['ftpServerAddress']
    except:
        return ""

def getOsPath():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Ftp-Info']['ftpOsPath']
    except:
        return ""

def getConfPath():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Ftp-Info']['ftpConfPath']
    except:
        return ""

def getIniConfPath():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Ftp-Info']['ftpIniConfPath']
    except:
        return ""


def getConsoleName():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Console-Info']['consoleUsername']
    except:
        return ""


def getConsoleAddress():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Console-Info']['consoleAddress']
    except:
        return ""


def getDatabaseAddress():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Console-Info']['databseAddress']
    except:
        return ""


def getDatabaseUsername():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Database-Info']['databseUsername']
    except:
        return ""

def getDatabaseConfTable():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Database-Info']['initConfigTable']
    except:
        return ""