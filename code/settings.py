import xmltodict
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from imagebutton import ImageButton
import messagewindow as msg

class SettingsModule:
    def __init__(self,window,layout):
        self.window = window
        self.layout = layout

    def settingsUI(self,window):
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(15)
        settingsVerticalContainer = QVBoxLayout(window)
        settingsVerticalContainer.setObjectName("verticalContainer")

        frame = QFrame()

        # Layout of top bar
        topBarLayout = QHBoxLayout()
        topBarLayout.setObjectName("topBarLayout")
        topBarLayout.setAlignment(Qt.AlignLeft)

        backButton = ImageButton(QPixmap("back.png"))
        backButton.setObjectName("backButton")
        backButton.clicked.connect(window.initialiseLauncher)
        topBarLayout.addWidget(backButton)
        frame.setLayout(topBarLayout)
        settingsVerticalContainer.addWidget(frame)

        # layout of below 3 boxes
        innerVerticalLayout = QVBoxLayout()
        innerVerticalLayout.setContentsMargins(0, 0, 0, 0)
        innerVerticalLayout.setObjectName("innerVerticalLayout")
        innerFrame = QFrame()
        innerContainer = QHBoxLayout()
        innerContainer.setSpacing(40)
        innerContainer.setContentsMargins(0, 0, 0, 0)
        innerContainer.setObjectName("innerContainer")

        ftpConfigLayout = QVBoxLayout()
        ftpConfigLayout.setObjectName("ftpConfigLayout")
        ftpConfigLayout.setSpacing(20)
        ftpConfigLabel = QLabel("FTP Configuration")
        ftpConfigLabel.setStyleSheet("background-color: rgb(0,188,212); border: 1px solid black; font-size:16px;")
        ftpConfigLayout.addWidget(ftpConfigLabel)
        self.ftpServerAddress = QLineEdit()
        self.ftpServerAddress.setPlaceholderText("Server Address")
        self.ftpServerAddress.setStyleSheet("background-color: rgb(255,255,255);")
        ftpConfigLayout.addWidget(self.ftpServerAddress)
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
        ftpConfigLabel = QLabel(
            "*Make sure to enable anonymous login on the FTP server to enable use of the deployment and maintenance module")
        ftpConfigLabel.setWordWrap(True);
        ftpConfigLabel.setStyleSheet(
            "color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        ftpConfigLayout.addWidget(ftpConfigLabel)
        ftpFrame = QFrame()
        ftpFrame.setLayout(ftpConfigLayout)
        ftpFrame.setStyleSheet(
            ".QFrame{ background-color: rgb(255,255,255); border: 1px solid black; font-size:16px; border-radius: 10px;}")
        ftpFrame.setContentsMargins(25, 0, 25, 5)
        ftpFrame.setGraphicsEffect(effect)
        innerContainer.addWidget(ftpFrame)

        consoleConfigLayout = QVBoxLayout()
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
        consoleConfigLabel.setStyleSheet(
            "color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        consoleConfigLabel.setWordWrap(True);
        consoleConfigLayout.addWidget(consoleConfigLabel)
        consoleConfigLabel = QLabel("*Example: port 700-748 -> on a 48 port console")
        consoleConfigLabel.setWordWrap(True);
        consoleConfigLabel.setStyleSheet(
            "color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        consoleConfigLayout.addWidget(consoleConfigLabel)

        consoleFrame = QFrame()
        consoleFrame.setLayout(consoleConfigLayout)
        consoleFrame.setStyleSheet(
            ".QFrame{ background-color: rgb(255,255,255); border: 1px solid black; font-size:16px; border-radius: 10px;}")
        consoleFrame.setContentsMargins(25, 0, 25, 5)
        consoleFrame.setGraphicsEffect(effect)
        innerContainer.addWidget(consoleFrame)

        databaseConfigLayout = QVBoxLayout()
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
        self.configTable = QLineEdit()
        self.configTable.setPlaceholderText("Configuration Table")
        self.configTable.setStyleSheet("background-color: rgb(255,255,255);")
        databaseConfigLayout.addWidget(self.configTable)

        databaseConfigLabel1 = QLabel(
            "*Ensure you input correct table names from your database to enable use of the deployment and maintenance module")
        databaseConfigLabel1.setWordWrap(True);
        databaseConfigLabel1.setStyleSheet(
            "color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        databaseConfigLayout.addWidget(databaseConfigLabel1)

        databaseFrame = QFrame()
        databaseFrame.setLayout(databaseConfigLayout)
        databaseFrame.setStyleSheet(
            ".QFrame{ background-color: rgb(255,255,255); border: 1px solid black; font-size:16px; border-radius: 10px;}")
        databaseFrame.setContentsMargins(25, 0, 25, 5)
        databaseFrame.setGraphicsEffect(effect)
        innerContainer.addWidget(databaseFrame)

        innerFrame.setContentsMargins(25, 25, 25, 25)
        innerFrame.setStyleSheet("background-color: rgb(96,125,139); border: 1px solid black; font-size:16px; ")

        innerVerticalLayout.addLayout(innerContainer)

        bottomLayout = QHBoxLayout()
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
        self.layout.setLayout(settingsVerticalContainer)
        self.fillSettingsFields()


    def fillSettingsFields(self):
        try:
            with open("Settings.xml") as file:
                settingsDict = xmltodict.parse(file.read())

            self.ftpServerAddress.setText(settingsDict['Settings']['Ftp-Info']['ftpServerAddress'])
            self.ftpOsPath.setText(settingsDict['Settings']['Ftp-Info']['ftpOsPath'])
            self.ftpConfPath.setText(settingsDict['Settings']['Ftp-Info']['ftpConfPath'])
            self.ftpIniConfPath.setText(settingsDict['Settings']['Ftp-Info']['ftpIniConfPath'])

            self.consoleAddress.setText(settingsDict['Settings']['Console-Info']['consoleAddress'])
            self.consoleUsername.setText(settingsDict['Settings']['Console-Info']['consoleUsername'])
            self.settingsFromPort.setText(settingsDict['Settings']['Console-Info']['settingsFromPort'])
            self.settingsToPort.setText(settingsDict['Settings']['Console-Info']['settingsToPort'])

            self.databseAddress.setText(settingsDict['Settings']['Database-Info']['databseAddress'])
            self.databseUsername.setText(settingsDict['Settings']['Database-Info']['databseUsername'])
            self.configTable.setText(settingsDict['Settings']['Database-Info']['configTable'])
            file.close()
            return True
        except:
            return False


    def allSettingsFieldsFilled(self):
        if len(self.ftpServerAddress.text()) < 1 \
                or len(self.ftpOsPath.text()) < 1 \
                or len(self.ftpConfPath.text()) < 1 \
                or len(self.ftpIniConfPath.text()) < 1 \
                or len(self.consoleAddress.text()) < 1 \
                or len(self.consoleUsername.text()) < 1 \
                or len(self.settingsFromPort.text()) < 1 \
                or len(self.settingsToPort.text()) < 1 \
                or len(self.databseAddress.text()) < 1 \
                or len(self.databseUsername.text()) < 1 \
                or len(self.configTable.text()) < 1:
            return False
        else:
            return True


    def applySettings(self):
        if self.allSettingsFieldsFilled():
            settings_file = open("Settings.xml", "w")
            osPath = makeLegalPath(self.ftpOsPath.text())
            confPath = makeLegalPath(self.ftpConfPath.text())
            iniconfPath = makeLegalPath(self.ftpIniConfPath.text())

            dict = {'Settings': {'Ftp-Info': {'ftpServerAddress': self.ftpServerAddress.text(),
                                              'ftpOsPath': osPath,
                                              'ftpConfPath': confPath,
                                              'ftpIniConfPath': iniconfPath},
                                 'Console-Info': {'consoleAddress': self.consoleAddress.text(),
                                                  'consoleUsername': self.consoleUsername.text(),
                                                  'settingsFromPort': self.settingsFromPort.text(),
                                                  'settingsToPort': self.settingsToPort.text()},
                                 'Database-Info': {'databseAddress': self.databseAddress.text(),
                                                   'databseUsername': self.databseUsername.text(),
                                                   'configTable': self.configTable.text()}}}
            xml = xmltodict.unparse(dict, pretty=True)
            settings_file.write(xml)
            settings_file.close()
            msg.messageWindow("Settings Saved","Your Settings are saved",False)
            self.initialiseLauncher()
            self.fillSettingsFields()
        else:
            msg.errorWindow("Empty Fields", "Please fill in all fields provided",True)

def makeLegalPath(path):
    if "/" in path[0] and "/" in path[len(path)-1]:
        return path
    elif "/" in path[0]:
        return path + "/"
    elif "/" in path[len(path)-1]:
        return "/" + path
    else:
        return "/" + path + "/"