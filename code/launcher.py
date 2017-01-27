import random
import sys
import threading
import connect_session
import scanner
import time
import os.path

import paramiko
import xmltodict
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ftplib import *

#Styling for progress bar
DEFAULT_STYLE = """

background-color: rgb(69,90,100);

}
"""

class windowLauncher(QWidget):
    def __init__(self):
        super(windowLauncher, self).__init__()
        self.setWindowTitle('Network Deployment Automation Maintenance Tool')
        self.setFixedSize(900, 700)

        self.blocked = False
        self.launcher = QWidget()
        self.deployment = QWidget()
        self.settings = QWidget()
        self.troubleshooting = QWidget()

        self.threads = []

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.launcher)
        self.Stack.addWidget(self.deployment)
        self.Stack.addWidget(self.settings)
        self.Stack.addWidget(self.troubleshooting)

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.Stack)

        self.setStyleSheet(DEFAULT_STYLE)
        self.setLayout(mainLayout)

        # check if settings file is setup
        if not os.path.isfile('./Settings.xml'):
            self.Stack.setCurrentIndex(2)
        else:
            self.Stack.setCurrentIndex(0)

        self.launcherUI()
        self.deploymentUI()
        self.settingsUI()
        self.troubleshootingUI()

        self.show()









    def launcherUI(self):

        verticalContainer = QVBoxLayout(self)

        settingsLayout = QHBoxLayout(self)
        settingsLayout.setContentsMargins(0,0,0,135)
        settingsLayout.addStretch()
        settingsButton = ImageButton(QPixmap("settings.png"))
        settingsButton.setObjectName("settingsButton")
        settingsButton.clicked.connect(self.initialiseSettings)
        settingsLayout.addWidget(settingsButton)
        verticalContainer.addLayout(settingsLayout)

        gridLayout = QGridLayout(self)
        deploymentButton = ImageButton(QPixmap("deployment.png"))
        deploymentButton.setObjectName("deploymentButton")
        deploymentButton.clicked.connect(self.initialiseDeployment)
        gridLayout.addWidget(deploymentButton, 0, 0, 1, 1)
        monitoringButton = ImageButton(QPixmap("monitoring.png"))
        monitoringButton.setObjectName("pushButton")
        monitoringButton.clicked.connect(self.initialiseMonitoring)
        gridLayout.addWidget(monitoringButton, 0, 1, 1, 1)
        troubleshootingButton = ImageButton(QPixmap("troubleshooting.png"))
        troubleshootingButton.setObjectName("pushButton_3")
        troubleshootingButton.clicked.connect(self.initialiseTroubleshooting)
        gridLayout.addWidget(troubleshootingButton, 0, 2, 1, 1)

        verticalContainer.addLayout(gridLayout)
        verticalContainer.addStretch()

        self.launcher.setLayout(verticalContainer)

    def settingsUI(self):
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(15)
        settingsVerticalContainer = QVBoxLayout(self)
        settingsVerticalContainer.setObjectName("verticalContainer")

        frame = QFrame()

        #Layout of top bar
        topBarLayout = QHBoxLayout(self)
        topBarLayout.setObjectName("topBarLayout")
        topBarLayout.setAlignment(Qt.AlignLeft)

        backButton = ImageButton(QPixmap("back.png"))
        backButton.setObjectName("backButton")
        backButton.clicked.connect(self.initialiseLauncher)
        topBarLayout.addWidget(backButton)
        frame.setLayout(topBarLayout)
        settingsVerticalContainer.addWidget(frame)

        #layout of below 3 boxes
        innerVerticalLayout = QVBoxLayout()
        innerVerticalLayout.setContentsMargins(0, 0, 0, 0)
        innerVerticalLayout.setObjectName("innerVerticalLayout")
        innerFrame = QFrame()
        innerContainer = QHBoxLayout(self)
        innerContainer.setSpacing(40)
        innerContainer.setContentsMargins(0, 0, 0, 0)
        innerContainer.setObjectName("innerContainer")

        ftpConfigLayout = QVBoxLayout(self)
        ftpConfigLayout.setObjectName("ftpConfigLayout")
        ftpConfigLayout.setSpacing(20)
        ftpConfigLabel = QLabel("FTP Configuration")
        ftpConfigLabel.setStyleSheet("background-color: rgb(0,188,212); border: 1px solid black; font-size:16px;")
        ftpConfigLayout.addWidget(ftpConfigLabel)
        self.ftpServerAddress = QLineEdit()
        self.ftpServerAddress.setPlaceholderText("Server Address")
        self.ftpServerAddress.setStyleSheet("background-color: rgb(255,255,255);")
        ftpConfigLayout.addWidget(self.ftpServerAddress)
        self.ftpUsername = QLineEdit()
        self.ftpUsername.setPlaceholderText("Username")
        self.ftpUsername.setStyleSheet("background-color: rgb(255,255,255);")
        ftpConfigLayout.addWidget(self.ftpUsername)
        self.ftpOsPath = QLineEdit()
        self.ftpOsPath.setPlaceholderText("OS Directory Path")
        self.ftpOsPath.setStyleSheet("background-color: rgb(255,255,255);")
        ftpConfigLayout.addWidget(self.ftpOsPath)
        self.ftpConfPath = QLineEdit()
        self.ftpConfPath.setPlaceholderText("Configuration Path")
        self.ftpConfPath.setStyleSheet("background-color: rgb(255,255,255);")
        ftpConfigLayout.addWidget(self.ftpConfPath)
        self.ftpIniConfPath = QLineEdit()
        self.ftpIniConfPath.setPlaceholderText("Initial Config Path")
        self.ftpIniConfPath.setStyleSheet("background-color: rgb(255,255,255);")
        ftpConfigLayout.addWidget(self.ftpIniConfPath)
        ftpConfigLabel = QLabel("*Make sure to enable anonymous login on the FTP server to enable use of the deployment and maintenance module")
        ftpConfigLabel.setWordWrap(True);
        ftpConfigLabel.setStyleSheet("color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        ftpConfigLayout.addWidget(ftpConfigLabel)
        ftpFrame = QFrame()
        ftpFrame.setLayout(ftpConfigLayout)
        ftpFrame.setStyleSheet(".QFrame{ background-color: rgb(255,255,255); border: 1px solid black; font-size:16px; border-radius: 10px;}")
        ftpFrame.setContentsMargins(25, 0, 25, 5)
        ftpFrame.setGraphicsEffect(effect)
        innerContainer.addWidget(ftpFrame)

        consoleConfigLayout = QVBoxLayout(self)
        consoleConfigLayout.setSpacing(35)
        consoleConfigLayout.setObjectName("consoleConfigLayout")

        consoleConfigLabel = QLabel("Console Server Configuration")
        consoleConfigLabel.setStyleSheet("background-color: rgb(0,188,212); border: 1px solid black; font-size:16px;")
        consoleConfigLayout.addWidget(consoleConfigLabel)
        self.consoleAddress = QLineEdit()
        self.consoleAddress.setPlaceholderText("Full Address")
        self.consoleAddress.setStyleSheet("background-color: rgb(255,255,255);")
        consoleConfigLayout.addWidget(self.consoleAddress)
        self.consoleUsername = QLineEdit()
        self.consoleUsername.setPlaceholderText("Username")
        self.consoleUsername.setStyleSheet("background-color: rgb(255,255,255);")
        consoleConfigLayout.addWidget(self.consoleUsername)
        self.settingsFromPort = QLineEdit()
        self.settingsFromPort.setPlaceholderText("> Port Range")
        self.settingsFromPort.setStyleSheet("background-color: rgb(255,255,255);")
        consoleConfigLayout.addWidget(self.settingsFromPort)
        self.settingsToPort = QLineEdit()
        self.settingsToPort.setPlaceholderText(">> Port Range")
        self.settingsToPort.setStyleSheet("background-color: rgb(255,255,255);")
        consoleConfigLayout.addWidget(self.settingsToPort)

        consoleConfigLabel = QLabel("*Specify amount of ports, Include any custom port assignments")
        consoleConfigLabel.setStyleSheet("color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        consoleConfigLabel.setWordWrap(True);
        consoleConfigLayout.addWidget(consoleConfigLabel)
        consoleConfigLabel = QLabel("*Example: port 700-748 -> on a 48 port console")
        consoleConfigLabel.setWordWrap(True);
        consoleConfigLabel.setStyleSheet("color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        consoleConfigLayout.addWidget(consoleConfigLabel)

        consoleFrame = QFrame()
        consoleFrame.setLayout(consoleConfigLayout)
        consoleFrame.setStyleSheet(".QFrame{ background-color: rgb(255,255,255); border: 1px solid black; font-size:16px; border-radius: 10px;}")
        consoleFrame.setContentsMargins(25, 0, 25, 5)
        consoleFrame.setGraphicsEffect(effect)
        innerContainer.addWidget(consoleFrame)

        databaseConfigLayout = QVBoxLayout(self)
        databaseConfigLayout.setSpacing(40)
        databaseConfigLayout.setObjectName("consoleConfigLayout")

        databaseConfigLabel = QLabel("Databse Configuration")
        databaseConfigLabel.setStyleSheet("background-color: rgb(0,188,212); border: 1px solid black; font-size:16px;")
        databaseConfigLayout.addWidget(databaseConfigLabel)
        self.databseAddress = QLineEdit()
        self.databseAddress.setPlaceholderText("Full Address")
        self.databseAddress.setStyleSheet("background-color: rgb(255,255,255);")
        databaseConfigLayout.addWidget(self.databseAddress)
        self.databseUsername = QLineEdit()
        self.databseUsername.setPlaceholderText("Username")
        self.databseUsername.setStyleSheet("background-color: rgb(255,255,255);")
        databaseConfigLayout.addWidget(self.databseUsername)
        self.initConfigTable = QLineEdit()
        self.initConfigTable.setPlaceholderText("Init config table")
        self.initConfigTable.setStyleSheet("background-color: rgb(255,255,255);")
        databaseConfigLayout.addWidget(self.initConfigTable)
        self.versionControlTable = QLineEdit()
        self.versionControlTable.setPlaceholderText("Version Control Table")
        self.versionControlTable.setStyleSheet("background-color: rgb(255,255,255);")
        databaseConfigLayout.addWidget(self.versionControlTable)

        databaseConfigLabel1 = QLabel("*Ensure you input correct table names from your database to enable use of the deployment and maintenance module")
        databaseConfigLabel1.setWordWrap(True);
        databaseConfigLabel1.setStyleSheet("color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        databaseConfigLayout.addWidget(databaseConfigLabel1)

        databaseFrame = QFrame()
        databaseFrame.setLayout(databaseConfigLayout)
        databaseFrame.setStyleSheet(".QFrame{ background-color: rgb(255,255,255); border: 1px solid black; font-size:16px; border-radius: 10px;}")
        databaseFrame.setContentsMargins(25, 0, 25, 5)
        databaseFrame.setGraphicsEffect(effect)
        innerContainer.addWidget(databaseFrame)

        innerFrame.setContentsMargins(25, 25, 25, 25)
        innerFrame.setStyleSheet("background-color: rgb(96,125,139); border: 1px solid black; font-size:16px; ")

        innerVerticalLayout.addLayout(innerContainer)


        bottomLayout = QHBoxLayout(self)
        bottomLayout.setObjectName("bottomLayout")
        applySettingsButton = QPushButton("Apply Settings")
        applySettingsButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
        applySettingsButton.clicked.connect(self.applySettings)
        bottomLayout.addWidget(applySettingsButton)



        innerVerticalLayout.addLayout(bottomLayout)
        innerFrame.setLayout(innerVerticalLayout)
        innerFrame.setGraphicsEffect(effect)
        settingsVerticalContainer.addWidget(innerFrame)

        settingsVerticalContainer.addStretch()
        self.settings.setLayout(settingsVerticalContainer)
        self.fillSettingsFields()

    def troubleshootingUI(self):
        verticalContainer = QVBoxLayout(self)
        verticalContainer.setObjectName("verticalContainer")

        topBarLayout = QHBoxLayout(self)
        topBarLayout.setObjectName("topBarLayout")
        topBarLayout.setSpacing(750)

        backButton = ImageButton(QPixmap("back.png"))
        backButton.setObjectName("backButton")
        backButton.clicked.connect(self.initialiseLauncher)
        topBarLayout.addWidget(backButton)
        refreshButton = ImageButton(QPixmap("refresh.png"))
        refreshButton.setObjectName("refreshButton")
        refreshButton.clicked.connect(self.refreshPage)
        refreshButton.setStyleSheet("height: 50px;")
        topBarLayout.addWidget(refreshButton)

        verticalContainer.addLayout(topBarLayout)
        innerContainer = QHBoxLayout(self)
        innerContainer.setContentsMargins(0, 0, 0, 0)
        innerContainer.setObjectName("innerContainer")

        detailsContainer = QVBoxLayout()
        loginContainer = QVBoxLayout()
        loginLabel = QLabel("Log into a device")
        loginLabel.setStyleSheet("background-color: rgb(0,188,212); border: 1px solid black; font-size:16px;")
        loginContainer.addWidget(loginLabel)
        self.deviceAddress = QLineEdit()
        self.deviceAddress.setPlaceholderText("Device Address")
        loginContainer.addWidget(self.deviceAddress)
        self.deviceUsername = QLineEdit()
        self.deviceUsername.setPlaceholderText("Device Username")
        loginContainer.addWidget(self.deviceUsername)
        self.devicePassword = QLineEdit()
        self.devicePassword.setPlaceholderText("Device Password")
        loginContainer.addWidget(self.devicePassword)
        loginButton = QPushButton("Connect to device")
        loginButton.setObjectName("deploymentButton")
        loginButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
        # mappingButton.clicked.connect(self.beginDeployment)
        loginContainer.addWidget(loginButton)

        loginFrame = QFrame()
        loginFrame.setLayout(loginContainer)
        loginFrame.setStyleSheet("background-color: white")
        detailsContainer.addWidget(loginFrame)

        statisticsContainer = QVBoxLayout()
        statisticsLabel = QLabel("Network Statistics")
        statisticsLabel.setStyleSheet("background-color: rgb(0,188,212); border: 1px solid black; font-size:16px;")
        statisticsContainer.addWidget(statisticsLabel)
        self.statisticsDetails = QTextEdit()
        self.statisticsDetails.setReadOnly(True)
        self.statisticsDetails.setText("When you log into a device it's details will appear here")
        statisticsContainer.addWidget(self.statisticsDetails)

        statisticsFrame = QFrame()
        statisticsFrame.setLayout(statisticsContainer)
        statisticsFrame.setStyleSheet("background-color: white")
        detailsContainer.addWidget(statisticsFrame)
        innerContainer.addLayout(detailsContainer)

        mapContainer = QVBoxLayout(self)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.image = QLabel()
        mapImage = QPixmap(dir_path + '\\network_path.png')
        mapImage = mapImage.scaled(mapImage.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.image.setPixmap(mapImage)
        self.image.mousePressEvent = self.getPos
        mapContainer.addWidget(self.image)
        self.scannerProgressBar = QProgressBar(self)
        self.scannerProgressBar.setProperty("value", 0)
        self.scannerProgressBar.setOrientation(Qt.Horizontal)
        self.scannerProgressBar.setTextVisible(False)
        self.scannerProgressBar.setObjectName("self.progressBar")
        self.scannerProgressBar.setStyleSheet("QProgressBar::chunk:horizontal { background-color: rgb(0,188,212);}")
        mapContainer.addWidget(self.scannerProgressBar)
        mappingButton = QPushButton("Start network mapping")
        mappingButton.setObjectName("deploymentButton")
        mappingButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
        mappingButton.clicked.connect(self.displayImage)
        mapContainer.addWidget(mappingButton)

        innerContainer.addLayout(mapContainer)
        verticalContainer.addLayout(innerContainer)

        self.troubleshooting.setLayout(verticalContainer)

    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(str(x) + " " +  str(y))

    def displayImage(self):
        if not self.blocked:
            self.blocked = True
            thread = NetworkScanner(self)
            thread.trigger.connect(self.updateScannerProgress)
            thread.setup(1)
            thread.start()
            self.threads.append(thread)
        else:
            QMessageBox.information(self, "Scan Running", "You're already running a network scan")

    def updateScannerProgress(self, percentage):
        if(percentage == 101):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            mapImage = QPixmap(dir_path + '\\network_path.png')
            mapImage = mapImage.scaled(mapImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image.setPixmap(mapImage)
            self.blocked = False
            self.scannerProgressBar.setValue(0)
        else:
            self.scannerProgressBar.setValue(percentage)


        #0 188 212
    #96 125 139
    def deploymentUI(self):
        verticalContainer = QVBoxLayout(self)
        verticalContainer.setObjectName("verticalContainer")

        topBarLayout = QHBoxLayout(self)
        topBarLayout.setObjectName("topBarLayout")
        topBarLayout.setSpacing(750)

        backButton = ImageButton(QPixmap("back.png"))
        backButton.setObjectName("backButton")
        backButton.clicked.connect(self.initialiseLauncher)
        topBarLayout.addWidget(backButton)
        refreshButton = ImageButton(QPixmap("refresh.png"))
        refreshButton.setObjectName("refreshButton")
        refreshButton.clicked.connect(self.refreshPage)
        refreshButton.setStyleSheet("height: 50px;")
        topBarLayout.addWidget(refreshButton)

        verticalContainer.addLayout(topBarLayout)

        innerContainer = QHBoxLayout(self)
        innerContainer.setContentsMargins(0, 0, 0, 0)
        innerContainer.setObjectName("innerContainer")

        loginFrame = QFrame()
        loginDetailsLayout = QGridLayout()
        loginDetailsLayout.setObjectName("loginDetailsLayout")
        loginDetailsLayout.setVerticalSpacing(50)
        portNoLayout = QGridLayout()
        portNoLayout.setObjectName("portNoLayout")
        label = QLabel("   TO   ")
        label.setObjectName("label")
        label.setStyleSheet("color:white; font-size:16px; border: 1px solid rgb(96,125,139);")
        portNoLayout.addWidget(label, 0, 1, 1, 1)
        self.fromPortNo = QLineEdit(self)
        self.fromPortNo.setObjectName("fromPortNo")
        self.fromPortNo.setStyleSheet("background-color: rgb(255,255,255);")
        self.fromPortNo.setPlaceholderText("> Port")
        portNoLayout.addWidget(self.fromPortNo, 0, 0, 1, 1)
        self.toPortNo = QLineEdit(self)
        self.toPortNo.setObjectName("toPortNo")
        self.toPortNo.setStyleSheet("background-color: rgb(255,255,255);")
        self.toPortNo.setPlaceholderText(">> Port")
        portNoLayout.addWidget(self.toPortNo, 0, 2, 1, 1)
        loginDetailsLayout.addLayout(portNoLayout, 1, 0, 1, 1)
        checkboxLayout = QVBoxLayout()
        checkboxLayout.setObjectName("checkboxLayout")
        
        self.willCloneToBackup = QCheckBox("Clone to Backup Partition")
        self.willCloneToBackup.setObjectName("self.willCloneToBackup")
        self.willCloneToBackup.setStyleSheet("color:white; font-size:16px; border: 1px solid rgb(96,125,139);")
        checkboxLayout.addWidget(self.willCloneToBackup)
        loginDetailsLayout.addLayout(checkboxLayout, 4, 0, 1, 1)

        deploymentButton = QPushButton("Begin Deployment")
        deploymentButton.setObjectName("deploymentButton")
        deploymentButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
        deploymentButton.clicked.connect(self.beginDeployment)
        loginDetailsLayout.addWidget(deploymentButton, 6, 0, 1, 1)


        self.consolePasswordField = QLineEdit(self)
        self.consolePasswordField.setPlaceholderText("Console Server Password")
        self.consolePasswordField.setEchoMode(QLineEdit.Password)
        self.consolePasswordField.setStyleSheet("background-color: rgb(255,255,255);")
        self.consolePasswordField.setObjectName("consolePasswordField")
        loginDetailsLayout.addWidget(self.consolePasswordField, 2, 0, 1, 1)

        self.ftpPasswordField = QLineEdit(self)
        self.ftpPasswordField.setPlaceholderText("FTP Server Password")
        self.ftpPasswordField.setEchoMode(QLineEdit.Password)
        self.ftpPasswordField.setStyleSheet("background-color: rgb(255,255,255);")
        self.ftpPasswordField.setObjectName("ftpPasswordField")
        loginDetailsLayout.addWidget(self.ftpPasswordField, 3, 0, 1, 1)
        
        self.osVersions = QComboBox(self)
        self.osVersions.setObjectName("self.osVersions")
        self.osVersions.setStyleSheet("background-color: rgb(255,255,255);")
        self.osFiles = self.getFiles(".tgz")
        self.osFiles.reverse()
        for index in range(len(self.osFiles)):
            self.osVersions.addItem(self.osFiles[index])

        loginDetailsLayout.addWidget(self.osVersions, 0, 0, 1, 1)

        configurationRangeFrame = QFrame()
        configurationRangeFrame.setContentsMargins(10,1,10,1)
        configurationRangeLayout = QVBoxLayout()
        configurationRangeLayout.setObjectName("configurationRangeLayout")
        #configurationRangeLayout.setSpacing(10)
        configurationRangeHeading = QLabel("Inital Configuration Range(Optional)")
        configurationRangeHeading.setObjectName("configurationRangeHeading")
        configurationRangeHeading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
        configurationRangeLayout.addWidget(configurationRangeHeading)
        
        self.fromConfiguration = QComboBox(self)
        self.fromConfiguration.setObjectName("fromConfiguration")
        self.fromConfiguration.setStyleSheet("background-color: rgb(255,255,255);")

        self.toConfiguration = QComboBox(self)
        self.toConfiguration.setObjectName("toConfiguration")
        self.toConfiguration.setStyleSheet("background-color: rgb(255,255,255);")

        self.confFiles = self.getFiles(".conf")
        self.confFiles.reverse()
        for index in range(len(self.confFiles)):
            self.fromConfiguration.addItem(self.confFiles[index])
            self.toConfiguration.addItem(self.confFiles[index])

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
        
        self.progressBar = QProgressBar(self)
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

        self.deployment.setLayout(verticalContainer)

    def getFiles(self,extension):

        try:
            ftpAddress = self.getFtpAddress()
            ftpAddress = "localhost"
            ftp = FTP(ftpAddress)
            ftp.login('filipSucksCock', 'password')
            files = ftp.nlst()
            actualFiles = []
            for index in range(len(files)):
                if (extension in files[index]):
                    actualFiles.append(files[index])
            return actualFiles

        except:
            return []

    def beginDeployment(self):
        #Make sure fields aren't empty
        if(self.fieldsEmpty()):
            QMessageBox.information(self, "Empty Fields", "Please ensure all the fields are filled")
            return
        #Make sure both port numbers are actually numbers
        if(not self.isNumber(self.toPortNo.text()) or not self.isNumber(self.fromPortNo.text())):
            QMessageBox.information(self, "Not a Number", "Please ensure ports are numbers")
            return

        #make sure configurations are the same amount as devices being updated
        fromConf = self.fromConfiguration.currentIndex()
        toConf = self.toConfiguration.currentIndex()
        fromPort = int(self.fromPortNo.text())
        toPort = int(self.toPortNo.text())
        if (not (toConf > fromConf)):
            QMessageBox.information(self, "Config List Error","Please ensure your starting configuration is before your final configuration")
            return
        if(not ((toConf - fromConf) + 1 == (toPort - fromPort) + 1)):
            QMessageBox.information(self, "Not Enough Configs", "Please ensure there are enough config files for each specified device")
            return


        #connect_session.patch_crypto_be_discovery()
        configurationsToUse = []
        for index in range(fromConf,toConf+1):
            configurationsToUse.append(self.confFiles[index])
        willBackup = self.willCloneToBackup.isChecked()
        ftpAddress = self.getFtpAddress()
        consoleAddress = self.getConsoleAddress()
        consoleUsername = self.getConsoleName()
        password = self.passwordField.text()
        self.progressBar.setValue(0)

        if(willBackup):
            print("Will clone to backup paritition")
        else:
            print("Will not clone to backup paritition")

        confIndex = fromConf
        #check to see how many devices we're updating
        if(toPort - fromPort + 1 == 1):
            print("Updating device at port " + str(toPort))
            thread = Updater(self)
            thread.trigger.connect(self.updateProgress)
            thread.setup(toPort,ftpAddress,consoleUsername,consoleAddress,password,configurationsToUse[confIndex],willBackup,True)
            thread.start()
            self.threads.append(thread)

        else:
            for index in range(fromPort,toPort):
                print("Updating device at port " + str(toPort))
                thread = Updater(self)
                thread.trigger.connect(self.updateProgress)
                thread.setup(index,ftpAddress,consoleUsername,consoleAddress,password,configurationsToUse[confIndex],willBackup,False)
                thread.start()
                self.threads.append(thread)
                confIndex += 1

            #make final thread the one to update GUI
            thread = Updater(self)
            thread.trigger.connect(self.updateProgress)
            thread.setup(toPort,ftpAddress,consoleUsername,consoleAddress,password,configurationsToUse[confIndex],willBackup,True)
            thread.start()
            self.threads.append(thread)


    def updateProgress(self, percentage):
        self.progressBar.setValue(percentage)
        if(percentage == 11):
            self.connectedToDevice.setStyleSheet("color:white; font-size:16px;")
        elif(percentage == 22):
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

    def fieldsEmpty(self):
        if(len(self.fromPortNo.text()) < 1 or len(self.toPortNo.text()) < 1 or len(self.passwordField.text()) < 1):
            return True
        else:
            return False

    def isNumber(self,number):
        try:
            int(number)
        except ValueError:
            return False
        else:
            return True


    def initialiseLauncher(self):
        if not os.path.isfile('./Settings.xml'):
            QMessageBox.information(self, "Settings", "You must fill in the information required to use this application")
        else:
            self.Stack.setCurrentIndex(0)
    def initialiseDeployment(self):
        self.Stack.setCurrentIndex(1)
    def initialiseMonitoring(self):
        print("Monitoring Module")
    def initialiseTroubleshooting(self):
        self.Stack.setCurrentIndex(3)
    def initialiseSettings(self):
        self.Stack.setCurrentIndex(2)
    def refreshPage(self):
        print("Refresh")

    def fillSettingsFields(self):
        try:
            with open("Settings.xml") as file:
                settingsDict = xmltodict.parse(file.read())

            self.ftpServerAddress.setText(settingsDict['Settings']['Ftp-Info']['ftpServerAddress'])
            self.ftpUsername.setText(settingsDict['Settings']['Ftp-Info']['ftpUsername'])
            self.ftpOsPath.setText(settingsDict['Settings']['Ftp-Info']['ftpOsPath'])
            self.ftpConfPath.setText(settingsDict['Settings']['Ftp-Info']['ftpConfPath'])
            self.ftpIniConfPath.setText(settingsDict['Settings']['Ftp-Info']['ftpIniConfPath'])

            self.consoleAddress.setText(settingsDict['Settings']['Console-Info']['consoleAddress'])
            self.consoleUsername.setText(settingsDict['Settings']['Console-Info']['consoleUsername'])
            self.settingsFromPort.setText(settingsDict['Settings']['Console-Info']['settingsFromPort'])
            self.settingsToPort.setText(settingsDict['Settings']['Console-Info']['settingsToPort'])

            self.databseAddress.setText(settingsDict['Settings']['Database-Info']['databseAddress'])
            self.databseUsername.setText(settingsDict['Settings']['Database-Info']['databseUsername'])
            self.initConfigTable.setText(settingsDict['Settings']['Database-Info']['initConfigTable'])
            self.versionControlTable.setText(settingsDict['Settings']['Database-Info']['versionControlTable'])
            file.close()
            return True
        except:
            return False


    def allSettingsFieldsFilled(self):
        if len(self.ftpServerAddress.text()) < 1 \
                or len(self.ftpUsername.text()) < 1\
                or len(self.ftpOsPath.text()) < 1\
                or len(self.ftpConfPath.text()) < 1\
                or len(self.ftpIniConfPath.text()) < 1\
                or len(self.consoleAddress.text()) < 1\
                or len(self.consoleUsername.text()) < 1\
                or len(self.settingsFromPort.text()) < 1 \
                or len(self.settingsToPort.text()) < 1 \
                or len(self.databseAddress.text()) < 1 \
                or len(self.databseUsername.text()) < 1 \
                or len(self.initConfigTable.text()) < 1 \
                or len(self.versionControlTable.text()) < 1:
            return False
        else:
            return True


    def applySettings(self):
        if self.allSettingsFieldsFilled():
            settings_file = open("Settings.xml", "w")
            dict ={'Settings':{'Ftp-Info':{'ftpServerAddress':self.ftpServerAddress.text(),
                   'ftpUsername':self.ftpUsername.text(),
                    'ftpOsPath':self.ftpOsPath.text(),
                    'ftpConfPath':self.ftpConfPath.text(),
                    'ftpIniConfPath':self.ftpIniConfPath.text()},
                    'Console-Info':{'consoleAddress':self.consoleAddress.text(),
                    'consoleUsername':self.consoleUsername.text(),
                    'settingsFromPort':self.settingsFromPort.text(),
                    'settingsToPort':self.settingsToPort.text()},
                   'Database-Info':{'databseAddress':self.databseAddress.text(),
                    'databseUsername':self.databseUsername.text(),
                    'initConfigTable':self.initConfigTable.text(),
                    'versionControlTable':self.versionControlTable.text()}}}
            xml = xmltodict.unparse(dict,pretty=True)
            settings_file.write(xml)
            settings_file.close()
            QMessageBox.information(self, "Settings Saved","Your Settings are saved")
            self.initialiseLauncher()
        else:
            QMessageBox.information(self, "Empty Fields", "Please fill in all fields provided")


    def display(self, i):
        self.Stack.setCurrentIndex(i)

    def getFtpAddress(self):
        try:
            with open("Settings.xml") as file:
                settingsDict = xmltodict.parse(file.read())
            return settingsDict['Settings']['Ftp-Info']['ftpServerAddress']
        except:
            return ""

    def getFtpName(self):
        try:
            with open("Settings.xml") as file:
                settingsDict = xmltodict.parse(file.read())
            return settingsDict['Settings']['Ftp-Info']['ftpUsername']
        except:
            return ""

    def getConsoleName(self):
        try:
            with open("Settings.xml") as file:
                settingsDict = xmltodict.parse(file.read())
            return settingsDict['Settings']['Ftp-Info']['consoleUsername']
        except:
            return ""

    def getConsoleAddress(self):
        try:
            with open("Settings.xml") as file:
                settingsDict = xmltodict.parse(file.read())
            return settingsDict['Settings']['Console-Info']['consoleAddress']
        except:
            return ""

class NetworkScanner(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(NetworkScanner, self).__init__(parent)

    def setup(self, thread_no):
        self.thread_no = thread_no

    def run(self):
        scanner.scanNetwork(self)


class Updater(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Updater, self).__init__(parent)

    def setup(self, thread_no,ftpAddress,consoleUsername,consoleAddress,password,configFile,willClone,isGUIUpdater):
        self.thread_no = thread_no
        self.ftpAddress = ftpAddress
        self.consoleUsername = consoleUsername
        self.consoleAddress = consoleAddress
        self.password = password
        self.willClone = willClone
        self.configFile = configFile
        self.isGUIUpdater = isGUIUpdater

    def run(self):
        self.connect_session(self.thread_no,self.consoleUsername,self.consoleAddress,self.password,self.ftpAddress,self.configFile,self.willClone,self.isGUIUpdater)


def connect_session(self,portNo, username, hostname, password,ftpAddress,configFile,willClone,updateGui):
    try:
        # replace port colon with underscore for filename
        filename = username + ":" + str(portNo) + ".xml"

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, 22, username, password)
        term = ssh.invoke_shell()
        if(updateGui):
            self.trigger.emit(11)
        connect_session.check(term, 5, "login")
        connect_session._login(term)
        if (updateGui):
            self.trigger.emit(22)
        connect_session.send_command(term, "set cli screen-length 0")

        xml = connect_session.send_command(term, "show chassis hardware | display xml")
        xml = xml[37:(len(xml)) - 10]
        text_file = open(filename, "w")
        text_file.write(xml)
        text_file.close()
        # parsing for serial
        connect_session.parse_xml_serial(filename, username)
        if (updateGui):
            self.trigger.emit(44)
        connect_session.send_command(term,"request system software add \"" + ftpAddress + "\" no-copy no-validate reboot")

        if (updateGui):
            self.trigger.emit(55)
        connect_session.check(term, 120, "login")
        connect_session._login(term)

        if (updateGui):
            self.trigger.emit(66)
        connect_session.send_command(term, "request system snapshot media internal slice alternate")
        # requested system snapshot
        connect_session.check(term, 60, "root")
        # partitioned snapshot
        connect_session.send_command(term, "set cli screen-length 0")
        # junos version check
        output = connect_session.send_command(term, "show system snapshot media internal | display xml")
        output = output[51:(len(output)) - 10]
        text_file = open(filename, "w")
        text_file.write(output)
        text_file.close()
        if (updateGui):
            self.trigger.emit(77)
        if (connect_session.parse_xml_version(filename, term)):
            connect_session.send_command(term, "delete /yes")
            connect_session.send_command(term, "load set \""+ ftpAddress  + "\"" + configFile)
            connect_session.send_command(term, "request system halt in 0")
            time.sleep(2)
            connect_session.send_command(term, "yes")
        else:
            QMessageBox.information(self, "Versions Not Configured", "OS versions not configured correctly")

        if (updateGui):
            self.trigger.emit(88)
        connect_session.send_command(term, "request system halt in 0")
        time.sleep(2)
        connect_session.send_command(term, "yes")
        ssh.close()
        if (updateGui):
            self.trigger.emit(100)
    except paramiko.ssh_exception.BadHostKeyException:
        QMessageBox.information(self, "Host Key Error!", "Server’s host key could not be verified")
    except paramiko.ssh_exception.AuthenticationException:
        QMessageBox.information(self, "Authentication Error!",
                                "Authentication failed, Check your details and try again")
    except paramiko.ssh_exception.SSHException:
        QMessageBox.information(self, "Unknown Error!", "Unknown error connecting or establishing an SSH session")


class ImageButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(ImageButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = windowLauncher()
    sys.exit(app.exec_())