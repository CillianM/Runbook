import socket
import time
from datetime import datetime
from ftplib import FTP

import paramiko
import pymysql
import xmltodict
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import secondaryWindows
from Connectivity import \
    checkDatabaseConnection,\
    checkConsoleConnection,\
    checkFTPConnection,\
    patch_crypto_be_discovery,\
    waitForLogin,\
    send_command,\
    waitForTerm
from customStyling import getTopBarLayout, IconLineEdit, getComboxboxStyle, ImageLable
from settings import \
    getIniConfPath, \
    getOsPath, \
    getDatabaseAddress, \
    getDatabaseUsername, \
    getFtpAddress, \
    getFtpUsername, \
    getConsoleAddress, \
    getConsoleName, getDatabase, getDatabaseTable

deploymentWindow = None


class DeploymentModule:
    def __init__(self, window, layout):
        self.layout = layout
        self.window = window
        self.blocked = False
        self.threads = []
        global deploymentWindow
        deploymentWindow = self

        self.ftpPassword = window.passwordManager.getFtpPassword()
        self.databasePassword = window.passwordManager.getDatabasePassword()

    #PyQt5 GUI setup
    def deploymentUI(self, window):
        try:
            self.consolePasswordField = IconLineEdit('./images/key.png', "Console Server Password",True)
            self.consolePasswordField.setWhatsThis("""This is the password for your console server it's required for the application to integrate with devices""")
            self.initialDevicePassword = IconLineEdit('./images/key.png', "Initial Device Password", True)
            self.initialDevicePassword.setWhatsThis("""You can choose what the initial password of each device will be, you can change individual device's password later on""")
            self.fromPortNo = IconLineEdit('./images/from.png', "From Port No.",False)
            self.fromPortNo.setWhatsThis("This is the FIRST port the devices are plugged into")
            self.toPortNo = IconLineEdit('./images/to.png', "To Port No.",False)
            self.toPortNo.setWhatsThis("This is the LAST port the devices are plugged into")
            self.willCloneToBackup = QCheckBox("Clone to Backup Partition")
            self.willCloneToBackup.setWhatsThis("If you would like to have each device clone the os to the backup partition then click here, if it's not available on the device then leave this box unchecked")
            self.osVersions = QComboBox()
            self.osVersions.setWhatsThis("Use this to select the OS you want to put on each device. it will be copied over from your FTP server to each device")
            self.fromConfiguration = QComboBox()
            self.fromConfiguration.setWhatsThis("Choose the FIRST in the list of configurations to apply to the devices")
            self.toConfiguration = QComboBox()
            self.fromConfiguration.setWhatsThis("Choose the LAST in the list of configurations to apply to the devices")
            verticalContainer = QVBoxLayout()
            verticalContainer.setObjectName("verticalContainer")

            topBarLayout = getTopBarLayout(self, window)
            verticalContainer.addLayout(topBarLayout)

            innerContainer = QHBoxLayout()
            innerContainer.setContentsMargins(0, 0, 0, 0)
            innerContainer.setObjectName("innerContainer")

            loginHeadLayout = QVBoxLayout()
            loginHeadLayout.addStretch()
            loginHeadLayout.setSpacing(0)
            loginLabel = ImageLable("images/hexagon.png", "Device Deployment Information           ")
            loginLabel.setStyleSheet("background-color: rgb(0,188,212);font-size:16px;")
            loginHeadLayout.addWidget(loginLabel.getWidget())

            loginFrame = QFrame()
            loginDetailsLayout = QGridLayout()
            loginDetailsLayout.setObjectName("loginDetailsLayout")
            loginDetailsLayout.setSpacing(36)

            self.osVersions.setObjectName("self.osVersions")
            self.osVersions.setStyleSheet(getComboxboxStyle())

            # Connect to ftp and get files for updating os
            self.osVersions.clear()
            self.osVersions.addItem("Loading")
            thread = FileGrabber(self.window)
            thread.setup(self, ".tgz",self.ftpPassword)
            thread.trigger.connect(self.fillComboBox)
            thread.start()
            self.threads.append(thread)

            loginDetailsLayout.addWidget(self.osVersions, 0, 0, 1, 1)

            portNoLayout = QGridLayout()
            portNoLayout.setObjectName("portNoLayout")
            label = QLabel("   TO   ")
            label.setObjectName("label")
            label.setStyleSheet("color:white; font-size:16px; border: 1px solid rgb(96,125,139);")
            portNoLayout.addWidget(label, 0, 1, 1, 1)

            portNoLayout.addWidget(self.fromPortNo.getWidget(), 0, 0, 1, 1)

            portNoLayout.addWidget(self.toPortNo.getWidget(), 0, 2, 1, 1)
            loginDetailsLayout.addLayout(portNoLayout, 1, 0, 1, 1)

            loginDetailsLayout.addWidget(self.consolePasswordField.getWidget(), 2, 0, 1, 1)

            loginDetailsLayout.addWidget(self.initialDevicePassword.getWidget(), 3, 0, 1, 1)

            checkboxLayout = QVBoxLayout()

            self.willCloneToBackup.setStyleSheet("color:white; font-size:16px; border: 1px solid rgb(96,125,139);")
            checkboxLayout.addWidget(self.willCloneToBackup)
            loginDetailsLayout.addLayout(checkboxLayout, 4, 0, 1, 1)

            configurationRangeFrame = QFrame()
            configurationRangeFrame.setContentsMargins(10, 1, 10, 1)
            configurationRangeLayout = QVBoxLayout()
            configurationRangeLayout.setObjectName("configurationRangeLayout")
            configurationRangeLayout.setSpacing(10)
            configurationRangeHeading = QLabel("Inital Configuration Range")
            configurationRangeHeading.setObjectName("configurationRangeHeading")
            configurationRangeHeading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
            configurationRangeLayout.addWidget(configurationRangeHeading)

            self.fromConfiguration.setObjectName("fromConfiguration")
            self.fromConfiguration.setStyleSheet(getComboxboxStyle())

            self.toConfiguration.setObjectName("toConfiguration")
            self.toConfiguration.setStyleSheet(getComboxboxStyle())

            # connect to ftp and get any files from ftp
            self.fromConfiguration.clear()
            self.toConfiguration.clear()
            self.fromConfiguration.addItem("Loading")
            self.toConfiguration.addItem("Loading")
            thread = FileGrabber(self.window)
            thread.setup(self, ".conf",self.ftpPassword)
            thread.trigger.connect(self.fillComboBox)
            thread.start()
            self.threads.append(thread)

            configurationRangeLayout.addWidget(self.fromConfiguration)
            configurationRangeLayout.addWidget(self.toConfiguration)
            configurationRangeFrame.setLayout(configurationRangeLayout)
            configurationRangeFrame.setStyleSheet("background-color: white; border: 1px solid black; font-size:16px; ")
            loginDetailsLayout.addWidget(configurationRangeFrame, 5, 0, 1, 1)
            loginDetailsLayout.setAlignment(Qt.AlignCenter)

            deploymentButton = QPushButton("Begin Deployment")
            deploymentButton.setObjectName("deploymentButton")
            deploymentButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
            deploymentButton.clicked.connect(self.beginDeployment)
            loginDetailsLayout.addWidget(deploymentButton, 6, 0, 1, 1)

            displayDbButton = QPushButton("Display Database")
            displayDbButton.setObjectName("displayDbButton")
            displayDbButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
            displayDbButton.clicked.connect(self.checkDatabase)
            loginDetailsLayout.addWidget(displayDbButton, 7, 0, 1, 1)

            loginFrame.setLayout(loginDetailsLayout)
            loginFrame.setStyleSheet("background-color: rgb(96,125,139); border: 1px solid black; font-size:16px; ")
            loginEffect = QGraphicsDropShadowEffect()
            loginEffect.setBlurRadius(15)
            loginFrame.setGraphicsEffect(loginEffect)

            loginHeadLayout.addWidget(loginFrame)
            innerContainer.addLayout(loginHeadLayout)

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
            self.progressBar.setStyleSheet("QProgressBar::chunk:vertical { background-color: rgb(0,188,212)}")

            progressBarLayout.addWidget(self.progressBar, 0, 0, 1, 1)

            progressBarLayout.setContentsMargins(50, 0, 50, 0)
            innerContainer.addLayout(progressBarLayout)

            progressTextFrame = QFrame()
            progressTextLayout = QGridLayout()

            progressTextLayout.setObjectName("progressTextLayout")
            progressTextLayout.setSpacing(43)
            deploymentProgressHeaderLayout = QVBoxLayout()
            deploymentProgressHeaderLayout.setSpacing(0)
            deploymentProgressHeaderLayout.addStretch()
            deploymentProgressHeader = ImageLable('./images/tick.png', "Deployment Progress")
            deploymentProgressHeader.setObjectName("deploymentProgressHeader")
            deploymentProgressHeader.setStyleSheet(
                "background-color: rgb(0,188,212);font-size:16px; height: 20px;")
            deploymentProgressHeaderLayout.addWidget(deploymentProgressHeader.getWidget())

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
            progressTextFrame.setStyleSheet(
                "background-color: rgb(96,125,139); border: 1px solid black; font-size:16px; ")
            progressTextEffect = QGraphicsDropShadowEffect()
            progressTextEffect.setBlurRadius(15)
            progressTextFrame.setGraphicsEffect(progressTextEffect)
            deploymentProgressHeaderLayout.addWidget(progressTextFrame)
            innerContainer.addLayout(deploymentProgressHeaderLayout)
            verticalContainer.addLayout(innerContainer)

            self.layout.setLayout(verticalContainer)
        except Exception as e:
            print(str(e))

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
        if percentage == 11:
            self.connectedToDevice.setStyleSheet("color:white; font-size:16px;")
        elif percentage == 22:
            self.loggedIn.setStyleSheet("color:white; font-size:16px;")
        elif percentage == 44:
            self.downloadingOS.setStyleSheet("color:white; font-size:16px;")
            self.installingOS.setStyleSheet("color:white; font-size:16px;")
        elif percentage == 55:
            self.rebootingDevice.setStyleSheet("color:white; font-size:16px;")
        elif percentage == 66:
            self.loggedInAgain.setStyleSheet("color:white; font-size:16px;")
        elif percentage == 77:
            self.applyingConfig.setStyleSheet("color:white; font-size:16px;")
        elif percentage == 88:
            self.rebootingTheDeviceAgain.setStyleSheet("color:white; font-size:16px;")
        else:
            self.blocked = False
            self.deploymentSuccessful.setStyleSheet("color:white; font-size:16px;")

    # fill appropriate combo box when code from thread is returned
    def fillComboBox(self, code):
        # deal with conf or tgz depending on code
        if code == 0:
            self.fromConfiguration.clear()
            self.toConfiguration.clear()
            for index in range(len(self.confFiles)):
                self.fromConfiguration.addItem(QIcon("images/from.png"),self.confFiles[index])
                self.toConfiguration.addItem(QIcon("images/to.png"),self.confFiles[index])
        elif code == 1:
            self.osVersions.clear()
            for index in range(len(self.osFiles)):
                self.osVersions.addItem(QIcon("images/device.png"),self.osFiles[index])

    # Refresh current page
    def refreshPage(self):
        try:
            if self.blocked:
                secondaryWindows.messageWindow("Process is currently running", "Cannot refresh page when units are being updated",
                                  False)
            else:
                self.fromConfiguration.addItem("Loading")
                self.toConfiguration.addItem("Loading")
                self.osVersions.addItem("Loading")
                self.clearProgressText()
                self.fromConfiguration.clear()
                self.toConfiguration.clear()
                thread = FileGrabber(self.window)
                thread.setup(self, ".conf",self.ftpPassword)
                thread.trigger.connect(self.fillComboBox)
                thread.start()
                self.threads.append(thread)

                thread = FileGrabber(self.window)
                thread.setup(self, ".tgz",self.ftpPassword)
                thread.trigger.connect(self.fillComboBox)
                thread.start()
                self.threads.append(thread)

                self.initialDevicePassword.setText("")
                self.consolePasswordField.setText("")
                self.willCloneToBackup.setChecked(False)
                self.toPortNo.setText("")
                self.fromPortNo.setText("")
        except Exception as e:
            print(str(e))
            secondaryWindows.messageWindow("Error Refreshing",
                              "An error occured clearing page and connecting to FTP server, try again later", True)

    def checkDatabase(self):
        if self.blocked:
            secondaryWindows.messageWindow("Process Running",
                                           "You're currently runnning an update, wait till this is finished",
                                           True)
            return

        if not checkDatabaseConnection(self.databasePassword):
            secondaryWindows.messageWindow("Database: Connection Error",
                                           "Error raised when connecting to Database, please check your details and try again",
                                           True)
            return

        listing = getDatabaseListing(self.databasePassword)
        if not listing is None:
            secondaryWindows.displayDatabaseWindow(listing)
        elif listing is None:
            secondaryWindows.messageWindow("Database is empty",
                                           "There is no data to pull from your database",
                                           False)
            return
        elif listing is "Error":
            secondaryWindows.messageWindow("Database Error",
                                           "There was an error pulling data from your database",
                                           True)

    def isNumber(self,s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    # makes sure there is at least one number in the password adn the length is > 6
    def checkValidity(self,string):
        if len(string) < 6:
            return False
        for i in range(0,len(string)):
            if self.isNumber(string[i]):
                return True
            elif string[i].isupper():
                return True

        return False

    def beginDeployment(self):
        try:
            # if the window is pressed twice
            if self.blocked:
                secondaryWindows.messageWindow("Process running.", "Please wait for deployment to finish.", True)
                return
            self.threads.clear()
            # Make sure fields aren't empty
            if self.fieldsEmpty():
                secondaryWindows.messageWindow("Empty Fields", "Please ensure all the fields are filled", True)
                return
            # Make sure both port numbers are actually numbers
            if (not isNumber(self.toPortNo.text()) or not isNumber(self.fromPortNo.text())):
                secondaryWindows.messageWindow("Not a Number", "Please ensure ports are numbers", True)
                return

            # make sure configurations are the same amount as devices being updated
            fromConf = self.fromConfiguration.currentIndex()
            toConf = self.toConfiguration.currentIndex()
            fromPort = int(self.fromPortNo.text())
            toPort = int(self.toPortNo.text())
            if not (toConf >= fromConf):
                secondaryWindows.messageWindow("Config List Error",
                                               "Please ensure your starting configuration is before your final configuration",
                                               True)
                return
            if not ((toConf - fromConf) + 1 == (toPort - fromPort) + 1):
                secondaryWindows.messageWindow("Not Enough Configs",
                                               "Please ensure there are enough config files for each specified device",
                                               True)
                return

            devicePassword = self.initialDevicePassword.text()
            if not self.checkValidity(devicePassword):
                secondaryWindows.messageWindow("Password error",
                                               """
                                               Please ensure the password is at least 6 characters and contains
                                               either a number or an uppercase letter
                                               """,
                                               True)
                return

            # apply patch
            patch_crypto_be_discovery()
            configurationsToUse = []
            for index in range(fromConf, toConf + 1):
                configurationsToUse.append(self.confFiles[index])

            willBackup = self.willCloneToBackup.isChecked()
            OsFile = self.osVersions.currentText()
            ftpPassword = self.ftpPassword
            consolePassword = self.consolePasswordField.text()
            databasePassword = self.databasePassword
            self.progressBar.setValue(0)

            # check if connections are accessible
            if not checkFTPConnection(ftpPassword):
                secondaryWindows.messageWindow("FTP: Connection Error",
                                               "Error raised when connecting to FTP server, please check your details and try again",
                                               True)
                return

            if not checkConsoleConnection(getConsoleAddress(), getConsoleName(), consolePassword):
                secondaryWindows.messageWindow("Console Server: Connection Error",
                                               "Error raised when connecting to Console server, please check your details and try again",
                                               True)
                return

            if not checkDatabaseConnection(databasePassword):
                secondaryWindows.messageWindow("Database: Connection Error",
                                               "Error raised when connecting to Database, please check your details and try again",
                                               True)
                return

            self.blocked = True

            confIndex = 0

            # check to see how many devices we're updating
            if toPort - fromPort + 1 == 1:
                thread = Updater(self.window)
                thread.trigger.connect(self.updateProgress)
                thread.setup(toPort, ftpPassword, consolePassword, databasePassword, devicePassword,OsFile, configurationsToUse[confIndex],
                             willBackup,
                             True)
                thread.start()
                self.threads.append(thread)

            else:
                for index in range(fromPort, toPort):
                    thread = Updater(self.window)
                    thread.trigger.connect(self.updateProgress)
                    thread.setup(index, ftpPassword, consolePassword, databasePassword, devicePassword, OsFile, configurationsToUse[confIndex],
                                 willBackup,
                                 False)
                    thread.start()
                    self.threads.append(thread)
                    confIndex += 1
                    time.sleep(5)  # staggered threads to avoid collision

                # make final thread the one to update GUI
                thread = Updater(self.window)
                thread.trigger.connect(self.updateProgress)
                thread.setup(toPort, ftpPassword, consolePassword, databasePassword, devicePassword, OsFile, configurationsToUse[confIndex],
                             willBackup,
                             True)
                thread.start()
                self.threads.append(thread)
        except Exception as e:
            print(str(e))

    def fieldsEmpty(self):
        if len(self.fromPortNo.text()) < 1 or len(self.toPortNo.text()) < 1 or len(
                self.consolePasswordField.text()) < 1:
            return True
        else:
            return False


# File grabber class to get files off UI thread
class FileGrabber(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(FileGrabber, self).__init__(parent)

    def setup(self, deploymentWindow, extension, password):
        self.deploymentWindow = deploymentWindow
        self.extension = extension
        self.password = password

    def run(self):
        if "conf" in self.extension:
            self.deploymentWindow.confFiles = getFiles(self.extension, self.password)
            self.trigger.emit(0)
        else:
            self.deploymentWindow.osFiles = getFiles(self.extension, self.password)
            self.trigger.emit(1)

def getFiles(extension,password):
    try:
        # anonymous login so no password
        if "conf" in extension:
            # set the ftp path to the config files location
            path = getIniConfPath()
        else:
            # set the ftp path to the os files location
            path = getOsPath()
        address = getFtpAddress()
        username = getFtpUsername()
        # Log into FTP
        ftp = FTP(address)
        ftp.login(username,password)
        ftp.cwd(path)

        # get list of all the files in the directory
        files = ftp.nlst()
        actualFiles = []
        # add all the files with the appropriate extension to the list
        for index in range(len(files)):
            if extension in files[index]:
                actualFiles.append(files[index])
        ftp.quit()
        return actualFiles

    except Exception as e:
        print(str(e))
        return [] #just return empty list no need for error

# Check if a number is given
def isNumber(number):
    try:
        int(number)
    except ValueError:
        return False
    else:
        return True

# Thread updater
class Updater(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Updater, self).__init__(parent)

    def setup(self, thread_no,ftpPassword,consolePassword, databsePassword, devicePassword, OsFile, configFile, willClone, isGUIUpdater):
        self.thread_no = thread_no
        self.ftpPassword = ftpPassword
        self.databsePassword = databsePassword
        self.consolePassword = consolePassword
        self.devicePassword = devicePassword
        self.willClone = willClone
        self.configFile = configFile
        self.isGUIUpdater = isGUIUpdater
        self.OsFile = OsFile

    def run(self):
        self.connect_session(self.thread_no, self.ftpPassword,self.consolePassword, self.databsePassword,self.devicePassword  ,self.OsFile, self.configFile,
                             self.willClone, self.isGUIUpdater)

    #Mian module functionality
    def connect_session(self, portNo, ftpPassword,consolePassword, databasePassword,devicePassword ,OsFile, configFile, willClone, updateGui):
        try:
            # Get values from user input
            ftpAddress = getFtpAddress()
            osFile = getOsPath() + OsFile
            confPath = getIniConfPath() + configFile
            username = getConsoleName() + ":" + str(portNo)
            hostname = getConsoleAddress()

            # Connect to the console server
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, 22, username, consolePassword)
            term = ssh.invoke_shell()

            # Log into the device
            if updateGui:
                self.trigger.emit(11)
            waitForTerm(term, 60, "login:")
            waitForLogin(term,devicePassword)
            if updateGui:
                self.trigger.emit(22)
            send_command(term, "set cli screen-length 0")

            # Get device serial number
            originalVersion = send_command(term, "show system software")
            xml = send_command(term, "show chassis hardware | display xml")
            serialNo = parse_xml_serial(xml)

            # Push serial number to the database
            updatedTime = pushSerial(getDatabaseAddress(), getDatabaseUsername(), databasePassword,getDatabase(), configFile, serialNo, confPath)
            if updateGui:
                self.trigger.emit(44)

            # Upgrade JUNOS
            ftpDetails = getFtpUsername() + ":" + ftpPassword + "@" + ftpAddress
            upgradeOs = "request system software add ftp://" + ftpDetails + osFile + " no-copy no-validate reboot"
            send_command(term, upgradeOs)

            # Wait for the device to reboot
            if updateGui:
                self.trigger.emit(55)
            print("upgrading")
            waitForTerm(term, 180, "login:")
            print("finished")
            waitForLogin(term,devicePassword)
            if updateGui:
                self.trigger.emit(66)
            waitForTerm(term, 2, "root")
            send_command(term, "set cli screen-length 0")

            # Snapshot to the backup partition
            if willClone:
                send_command(term, "request system snapshot media internal slice alternate")
            time.sleep(15)
            waitForTerm(term, 60, "root")

            # Check the version of JUNOS
            updatedVersion = send_command(term, "show system software")
            if updateGui:
                self.trigger.emit(77)

            # Start applying a configuration to the device
            if not updatedVersion == originalVersion:
                send_command(term, "configure")
                time.sleep(2)
                send_command(term, "delete")
                time.sleep(2)
                send_command(term, "yes")
                time.sleep(2)
                # Get the configuration file from the FTP Server
                send_command(term, "load set ftp://" + ftpAddress + confPath)
                time.sleep(2)
                xml = send_command(term, "show snmp location | display xml")
                time.sleep(2)

                # Get device deployment location (rollNo)
                rollNo = ""
                try:
                    xml = xml.split("<rpc-reply")[1]
                    xml = "<rpc-reply" + xml
                    xml = xml.split("</rpc-reply>")[0]
                    xml += "</rpc-reply>"
                    xmlDict = xmltodict.parse(xml)
                    rollNo = xmlDict['rpc-reply']['configuration']['snmp']['location']
                except:
                    print ("No location data.")
                time.sleep(5)

                # Push roll number (deployment location) to the database
                pushRollNo(getDatabaseAddress(), getDatabaseUsername(), databasePassword,getDatabase(),rollNo, updatedTime)
                time.sleep(5)

                #Set device root password
                send_command(term,"set system root-authentication plain-text-password")
                send_command(term,devicePassword)
                send_command(term,devicePassword) #confirm password
                time.sleep(2)

                #Commit the current configuration
                send_command(term, "commit and-quit")
                waitForTerm(term, 60, "root@")
                send_command(term, "request system autorecovery state save")
                time.sleep(30)
                send_command(term, "request system configuration rescue save")
                time.sleep(30)

                # Update the progress bar
                if updateGui:
                    self.trigger.emit(88)

                # Reboot the device
                send_command(term, "request system reboot")
                time.sleep(2)
                send_command(term, "yes")

                #Wait for the device to boot
                waitForTerm(term, 180, "login:")
                time.sleep(2)

                # Log into the device
                waitForLogin(term, devicePassword)
                waitForTerm(term, 10, "root")
                xml = send_command(term, "show configuration snmp location | display xml")
                time.sleep(5)

                # Get device deployment location (rollNo) - in order to perform a final check
                checkRollNo=""
                try:
                    xml = xml.split("<rpc-reply")[1]
                    xml = "<rpc-reply" + xml
                    xml = xml.split("</rpc-reply>")[0]
                    xml += "</rpc-reply>"
                    xmlDict = xmltodict.parse(xml)
                    checkRollNo = xmlDict['rpc-reply']['configuration']['snmp']['location']
                except:
                    print("No location data.")

                if rollNo == checkRollNo:
                    print("Deployment successful.")
                    send_command(term, "request system halt in 0")
                    time.sleep(2)
                    send_command(term, "yes")

                if updateGui:
                    self.trigger.emit(100)
            else:
                print("OS wasn't updated correctly, Not applying config, Shutting down")

        except paramiko.ssh_exception.BadHostKeyException:
            secondaryWindows.messageWindow("Host Key Error!", "Server’s host key could not be verified", True)
        except paramiko.ssh_exception.AuthenticationException:
            secondaryWindows.messageWindow("Authentication Error!", "Authentication failed, Check your details and try again", True)
        except paramiko.ssh_exception.SSHException:
            secondaryWindows.messageWindow("Unknown Error!", "Unknown error connecting or establishing an SSH session", True)
        except socket.gaierror as e:
            print(str(e))

# Push the device serial nuber to the database
def pushSerial(dbAddress, dbUsername, dbPassword,db ,configFileName, serialNo, configFile):
    time = getTime()
    configFileName = configFileName.split(".conf")[0]
    configTable = 'configurations'
    sql = ("insert into " + configTable + "(name,serial,user,path,timestamp,isprimary) values (\"" + configFileName + "\", \"" + serialNo + "\",\"" + dbUsername + "\",\"" + configFile + "\",\"" + time + "\",1)")

    conn = None

    try:
        conn = pymysql.connect(host=dbAddress, port=3306, user=dbUsername, passwd=dbPassword, db=db)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()

    except Exception as e:
        print("Error connecting to the database: " + str(e))
        if not cursor is None:
            cursor.close()
        if not conn is None:
            conn.close()
        return "Error"

    return time

# Push the device location to the database
def pushRollNo(dbAddress, dbUsername, dbPassword,db ,rollNo, updatedTime):
    configTable = 'configurations'
    sql = ("update " + configTable + " set title=\"Initial Configuration\", description=\"" + rollNo + "\" where timestamp=\"" + updatedTime + "\"")

    conn = None

    try:
        conn = pymysql.connect(host=dbAddress, port=3306, user=dbUsername, passwd=dbPassword, db=db)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("Error connecting to the database: " + str(e))
        if not cursor is None:
            cursor.close()
        if not conn is None:
            conn.close()
        return "Error"

# Parse the xml output for the device serial number
def parse_xml_serial(xml):
    try:
        xml = xml.split("<rpc-reply")[1]
        xml = "<rpc-reply" + xml
        xml = xml.split("</rpc-reply>")[0]
        xml += "</rpc-reply>"
        xmlDict = xmltodict.parse(xml)
        return xmlDict['rpc-reply']['chassis-inventory']['chassis']['serial-number']
    except:
        return "Serial number parsing error."

# Generate a timestamp
def getTime():
    return datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f')[:-4]

# Get a listing of up to 100 elements in the database
def getDatabaseListing(dbPswd):
    dbAddr = getDatabaseAddress()
    dbUsr = getDatabaseUsername()
    database = getDatabase()
    table = getDatabaseTable()

    conn = None
    cursor = None

    try:
        conn = pymysql.connect(host=dbAddr, port=3306, user=dbUsr, passwd=dbPswd, db=database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+ table+" limit 100;") # return a limit of 100 listings
        response = cursor.fetchall()
        if response:  # if we've returned something
            cursor.close()
            conn.close()
            return response
        else:
            cursor.close()
            conn.close()
            return None
    except pymysql.OperationalError:
        return None
    except:  # any issue assume no clear connection to database
        if not cursor is None:
            cursor.close()
        if not conn is None:
            conn.close()
        return "Error"