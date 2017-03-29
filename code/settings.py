import time
import xmltodict
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from customStyling import ImageButton, IconLineEdit, ImageLable
import secondaryWindows

# Used when setting up the application initially
class SettingsModule:
    def __init__(self,window,layout):
        self.window = window
        self.layout = layout
        self.restart = False

    # Setting GUI
    def settingsUI(self,window):
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(15)
        settingsVerticalContainer = QVBoxLayout()
        settingsVerticalContainer.setObjectName("verticalContainer")

        frame = QFrame()

        # Layout of top bar
        topBarLayout = QHBoxLayout()
        topBarLayout.setObjectName("topBarLayout")
        topBarLayout.setAlignment(Qt.AlignLeft)

        backButton = ImageButton(QPixmap("images/back.png"))
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
        innerContainer.setContentsMargins(0, 0, 0, 0)
        innerContainer.setObjectName("innerContainer")

        ftpHeadingLayout = QVBoxLayout()
        ftpHeadingLayout.setSpacing(0)
        ftpHeadingLayout.addStretch()
        ftpConfigLabel = ImageLable('./images/hexagon.png', "FTP Configuration")
        ftpConfigLabel.setStyleSheet(("""
                                            background-color: rgb(0,188,212);
                                            font-size:16px;
                                            border-top-left-radius: 10px;
                                            border-top-right-radius: 10px;
                                         """))
        ftpHeadingLayout.addWidget(ftpConfigLabel.getWidget())

        ftpConfigLayout = QVBoxLayout()
        ftpConfigLayout.setObjectName("ftpConfigLayout")
        ftpConfigLayout.setSpacing(40)
        self.ftpServerAddress = IconLineEdit('./images/device.png', "Server Address",False)
        self.ftpServerAddress.setWhatsThis("Input where you're FTP server is located")
        ftpConfigLayout.addWidget(self.ftpServerAddress.getWidget())
        self.ftpUsername = IconLineEdit('./images/user.png', "FTP Username", False)
        self.ftpUsername.setWhatsThis("This is your username for the FTP server")
        ftpConfigLayout.addWidget(self.ftpUsername.getWidget())
        self.ftpOsPath = IconLineEdit('./images/device.png', "OS Directory Path",False)
        self.ftpOsPath.setWhatsThis("Set the directory in your FTP server for where you keep your .tgz OS files so the application can point to them when deploying devices")
        ftpConfigLayout.addWidget(self.ftpOsPath.getWidget())
        self.ftpConfPath = IconLineEdit('./images/device.png', "Configuration Path",False)
        self.ftpConfPath.setWhatsThis("Set a directory in your FTP server for new .conf files to be pushed to")
        ftpConfigLayout.addWidget(self.ftpConfPath.getWidget())
        self.ftpIniConfPath  = IconLineEdit('./images/device.png', "Initial Config Path",False)
        self.ftpIniConfPath.setWhatsThis("Set the directory in your FTP server for where you keep your .conf files that have yet to be applied to devices so the application can point to them when deploying devices")
        ftpConfigLayout.addWidget(self.ftpIniConfPath.getWidget())
        ftpConfigLabel = QLabel(
            "*This will be used to push and pull config files for your device as you work")
        ftpConfigLabel.setWordWrap(True);
        ftpConfigLabel.setStyleSheet(
            "color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        ftpConfigLayout.addWidget(ftpConfigLabel)
        ftpFrame = QFrame()
        ftpFrame.setObjectName("ftpFrame")
        ftpFrame.setLayout(ftpConfigLayout)
        ftpFrame.setStyleSheet(
            """
            QFrame#ftpFrame
            {
            background-color: rgb(255,255,255); border: 1px solid black; font-size:16px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px
            }
            """)
        ftpFrame.setContentsMargins(25, 0, 25, 5)
        ftpFrame.setGraphicsEffect(effect)
        ftpHeadingLayout.addWidget(ftpFrame)
        innerContainer.addLayout(ftpHeadingLayout)

        consoleHeadingLayout = QVBoxLayout()
        consoleHeadingLayout.setSpacing(0)
        consoleHeadingLayout.addStretch()
        consoleConfigLabel = ImageLable('./images/hexagon.png', "Console Server Configuration")
        consoleConfigLabel.setStyleSheet(("""
                                            background-color: rgb(0,188,212);
                                            font-size:16px;
                                            border-top-left-radius: 10px;
                                            border-top-right-radius: 10px;
                                         """))
        consoleHeadingLayout.addWidget(consoleConfigLabel.getWidget())


        consoleConfigLayout = QVBoxLayout()
        consoleConfigLayout.setObjectName("consoleConfigLayout")
        consoleConfigLayout.setSpacing(146)
        self.consoleAddress = IconLineEdit('./images/device.png', "Full Console Address",False)
        self.consoleAddress.setWhatsThis("Set the address for your console server")
        consoleConfigLayout.addWidget(self.consoleAddress.getWidget())
        self.consoleUsername = IconLineEdit('./images/user.png', "Username",False)
        self.consoleUsername.setWhatsThis("Set the username for your console server")
        consoleConfigLayout.addWidget(self.consoleUsername.getWidget())

        consoleConfigLabel = QLabel("*To allow for bulk updates your console server's info will be required here")
        consoleConfigLabel.setStyleSheet(
            "color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        consoleConfigLabel.setWordWrap(True);
        consoleConfigLayout.addWidget(consoleConfigLabel)

        consoleFrame = QFrame()
        consoleFrame.setLayout(consoleConfigLayout)
        consoleFrame.setObjectName("consoleFrame")
        consoleFrame.setStyleSheet(
            """
            QFrame#consoleFrame
            {
            background-color: rgb(255,255,255); border: 1px solid black; font-size:16px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px
            }
            """)
        consoleFrame.setContentsMargins(25, 0, 25, 5)
        consoleFrame.setGraphicsEffect(effect)
        consoleHeadingLayout.addWidget(consoleFrame)
        innerContainer.addLayout(consoleHeadingLayout)

        datbaseHeadingLayout = QVBoxLayout()
        datbaseHeadingLayout.setSpacing(0)
        datbaseHeadingLayout.addStretch()
        databaseConfigLabel = ImageLable('./images/hexagon.png', "Database Configuration")
        databaseConfigLabel.setStyleSheet(("""
                                            background-color: rgb(0,188,212);
                                            font-size:16px;
                                            border-top-left-radius: 10px;
                                            border-top-right-radius: 10px;
                                            """))
        datbaseHeadingLayout.addWidget(databaseConfigLabel.getWidget())

        databaseConfigLayout = QVBoxLayout()
        databaseConfigLayout.setObjectName("consoleConfigLayout")
        databaseConfigLayout.setSpacing(138)
        self.databseAddress = IconLineEdit('./images/device.png', "Full Database Address",False)
        self.databseAddress.setWhatsThis("Set the address for your database")
        databaseConfigLayout.addWidget(self.databseAddress.getWidget())
        self.databseUsername = IconLineEdit('./images/user.png', "Username",False)
        self.databseUsername.setWhatsThis("Set the username for your database")
        databaseConfigLayout.addWidget(self.databseUsername.getWidget())

        databaseConfigLabel = QLabel(
            "*This database will be used to track updated devices and their config files as you work")
        databaseConfigLabel.setWordWrap(True);
        databaseConfigLabel.setStyleSheet(
            "color: rgb(0,188,212); font-size:16px; background-color: rgb(255,255,255); border: 1px solid white;")
        databaseConfigLayout.addWidget(databaseConfigLabel)



        databaseFrame = QFrame()
        databaseFrame.setLayout(databaseConfigLayout)
        databaseFrame.setObjectName("databaseFrame")
        databaseFrame.setStyleSheet(
            """
            QFrame#databaseFrame{
            background-color: rgb(255,255,255); border: 1px solid black; font-size:16px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px
            }
            """)
        databaseFrame.setContentsMargins(25, 0, 25, 5)
        databaseFrame.setGraphicsEffect(effect)
        datbaseHeadingLayout.addWidget(databaseFrame)
        innerContainer.addLayout(datbaseHeadingLayout)

        innerFrame.setContentsMargins(25, 25, 25, 25)
        innerFrame.setObjectName("innerFrame")
        innerFrame.setStyleSheet("QFrame#innerFrame{ background-color: rgb(96,125,139); border: 1px solid black; font-size:16px} ")

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

    # Set placeholder text
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

            self.databseAddress.setText(settingsDict['Settings']['Database-Info']['databseAddress'])
            self.databseUsername.setText(settingsDict['Settings']['Database-Info']['databseUsername'])
            file.close()
            return True
        except:
            return False

    # Check if all settings fiels have been filled
    def allSettingsFieldsFilled(self):
        if len(self.ftpServerAddress.text()) < 1 \
                or len(self.ftpUsername.text()) < 1 \
                or len(self.ftpOsPath.text()) < 1 \
                or len(self.ftpConfPath.text()) < 1 \
                or len(self.ftpIniConfPath.text()) < 1 \
                or len(self.consoleAddress.text()) < 1 \
                or len(self.consoleUsername.text()) < 1 \
                or len(self.databseAddress.text()) < 1 \
                or len(self.databseUsername.text()) < 1:
            return False
        else:
            return True

    # Save settings fields to a xml file
    def applySettings(self):
        if self.allSettingsFieldsFilled():
            try:
                #settings are saved in xml file
                settings_file = open("Settings.xml", "w")
                #ensure paths are "legal"
                osPath = self.makeLegalPath(self.ftpOsPath.text())
                confPath = self.makeLegalPath(self.ftpConfPath.text())
                iniconfPath = self.makeLegalPath(self.ftpIniConfPath.text())

                #construct dict to be translated into xml
                dict = {'Settings': {'Ftp-Info': {'ftpServerAddress': self.ftpServerAddress.text(),
                                                  'ftpUsername':self.ftpUsername.text(),
                                                  'ftpOsPath': osPath,
                                                  'ftpConfPath': confPath,
                                                  'ftpIniConfPath': iniconfPath},
                                     'Console-Info': {'consoleAddress': self.consoleAddress.text(),
                                                      'consoleUsername': self.consoleUsername.text()},
                                     'Database-Info': {'databseAddress': self.databseAddress.text(),
                                                       'databseUsername': self.databseUsername.text()}}}
                #convert dict
                xml = xmltodict.unparse(dict, pretty=True)
                #write dict to file
                settings_file.write(xml)
                settings_file.close()
                #alert user to success
                if self.window.notSetup:
                    heading = "Settings Saved! Restarting in 3...."
                    message = "Your Settings are saved, The programme will restart and reload the changes"
                    self.restart = True
                else:
                    heading = "Settings Saved!"
                    message = "Your Settings are saved"
                secondaryWindows.messageWindow(heading,message,False)
                if self.window.notSetup:
                    time.sleep(3)
                    self.window.close()
                else:
                    self.window.initialiseLauncher()

            #catch any exceptions when writing to file and cope gracefully
            except Exception as e:
                secondaryWindows.messageWindow("An Error Occured", "There was an error saving your settings the details are as follows: \n " + str(e), True)
        else:
            secondaryWindows.messageWindow("Empty Fields", "Please fill in all fields provided",True)

    #Ensure that the paths being put in are legal (ie. slash at the start and end)
    def makeLegalPath(self,path):
        if "/" in path[0] and "/" in path[len(path)-1]:
            return path
        elif "/" in path[0]:
            return path + "/"
        elif "/" in path[len(path)-1]:
            return "/" + path
        else:
            return "/" + path + "/"

# --- Get values from setting fields ---
def getFtpAddress():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Ftp-Info']['ftpServerAddress']
    except:
        return "Could not get FTP address."

def getFtpUsername():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Ftp-Info']['ftpUsername']
    except:
        return "Cannot get the FTP username."


def getOsPath():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Ftp-Info']['ftpOsPath']
    except:
        return "Cannot get the OS path."


def getConfPath():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Ftp-Info']['ftpConfPath']
    except:
        return "Cannot get the configuration path."


def getIniConfPath():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Ftp-Info']['ftpIniConfPath']
    except:
        return "Cannot get the initial configuration path."


def getConsoleName():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Console-Info']['consoleUsername']
    except:
        return "Cannot get the console name."


def getConsoleAddress():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Console-Info']['consoleAddress']
    except:
        return "Cannot get the console address."


def getDatabaseAddress():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Database-Info']['databseAddress']
    except:
        return "Cannot get the database address."


def getDatabaseUsername():
    try:
        with open("Settings.xml") as file:
            settingsDict = xmltodict.parse(file.read())
        return settingsDict['Settings']['Database-Info']['databseUsername']
    except:
        return "Cannot get the databaseusername."

# Minor functions to allow for maintainability
def getDatabaseTable():
    return 'configurations'

def getDatabase():
    return 'runbook'