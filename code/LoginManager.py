'''
Class allows for the structured initialisation of the programme along
with a structured way to set and get the entered passwords
'''

from Connectivity import checkDatabaseConnection, checkFTPConnection
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from customStyling import ImageLable, IconLineEdit
from secondaryWindows import messageWindow


class LoginManager():
    def __init__(self, passwordManager):
        super(LoginManager, self).__init__()
        self.passwordManager = passwordManager
        self.dialog = None
        self.databasePasswordField = None
        self.ftpPasswordField = None
        self.passwordsEntered = False
        self.wantsSettings = False

    def getPasswordsAlert(self):
        self.dialog = QDialog()
        self.dialog.setWindowIcon(QIcon('images/icon.ico'))
        self.dialog.setWindowTitle("Login Details")
        self.dialog.setStyleSheet("background-color: rgb(69,90,100);")
        self.dialog.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        mainLayout = QVBoxLayout(self.dialog)

        loginHeadLayout = QVBoxLayout()
        loginHeadLayout.setContentsMargins(25, 25, 25, 25)
        loginHeadLayout.addStretch()
        loginHeadLayout.setSpacing(0)
        loginLabel = ImageLable("images/tick.png", "  Login Credentials")
        loginLabel.setWhatsThis("To use the application we need to access the FTP directories & the database you set up")
        loginLabel.setStyleSheet("background-color: rgb(0,188,212);font-size:16px;")
        loginLabel.setContentsMargins(25, 25, 25, 25)
        loginHeadLayout.addWidget(loginLabel.getWidget())

        detailsFrame = QFrame()
        detailsFrame.setContentsMargins(25, 25, 25, 25)
        detailsLayout = QVBoxLayout()
        detailsLayout.setSpacing(10)

        self.databasePasswordField = IconLineEdit('./images/key.png', "Database Password", True)
        detailsLayout.addWidget(self.databasePasswordField.getWidget())

        self.ftpPasswordField = IconLineEdit('./images/key.png', "FTP Password", True)
        detailsLayout.addWidget(self.ftpPasswordField.getWidget())

        loginButton = QPushButton("Login")
        loginButton.setObjectName("loginButton")
        loginButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
        loginButton.clicked.connect(self.closeWindow)
        detailsLayout.addWidget(loginButton)

        settingsButton = QPushButton("Edit Settings")
        settingsButton.setObjectName("loginButton")
        settingsButton.setStyleSheet("background-color: rgb(192,192,192); font-size:16px;")
        settingsButton.clicked.connect(self.initialiseSettings)
        detailsLayout.addWidget(settingsButton)

        detailsFrame.setLayout(detailsLayout)
        detailsFrame.setStyleSheet("border: 1px solid black; background-color: rgb(96,125,139);")
        loginHeadLayout.addWidget(detailsFrame)
        mainLayout.addLayout(loginHeadLayout)

        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.dialog.exec_()

    def initialiseSettings(self):
        self.wantsSettings = True
        self.dialog.close()

    # when closing the window, check if the passwords are legal ones and if so then allow us to continue
    def closeWindow(self):
        tmpDbPassword = self.databasePasswordField.text()
        tmpFtpPassword = self.ftpPasswordField.text()
        if checkDatabaseConnection(tmpDbPassword):
            if checkFTPConnection(tmpFtpPassword):
                self.passwordManager.setDatabasePassword(self.databasePasswordField.text())
                self.passwordManager.setFtpPassword(self.ftpPasswordField.text())
                self.passwordsEntered = True
                self.dialog.close()
            else:
                messageWindow("FTP: Connection Error",
                              "Error raised when connecting to FTP, please check your details and try again",
                              True)
                self.databasePasswordField.setText("")
                self.ftpPasswordField.setText("")
        else:
            messageWindow("Database: Connection Error",
                          "Error raised when connecting to Database server, please check your details and try again",
                          True)
            self.databasePasswordField.setText("")
            self.ftpPasswordField.setText("")

# class to store and hand out the passwords entered
class PasswordManager():
    def __init__(self):
        super(PasswordManager, self).__init__()
        self.dbPassword = None
        self.ftpPassword = None

    def getDatabasePassword(self):
        return self.dbPassword

    def getFtpPassword(self):
        return self.ftpPassword

    def setDatabasePassword(self, dbPassword):
        self.dbPassword = dbPassword

    def setFtpPassword(self, ftpPassword):
        self.ftpPassword = ftpPassword