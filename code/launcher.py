import os.path
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from LoginManager import LoginManager,PasswordManager
from customStyling import ImageButton
from deployment import DeploymentModule
from maintenance import MaintenanceModule
from settings import SettingsModule
from troubleshooting import TroubleshootingModule

#Styling for progress bar
DEFAULT_STYLE = """
QWidget {
background-color: rgb(69,90,100);
}


"""

# Launch the main application window
class windowLauncher(QWidget):

    def __init__(self):
        super(windowLauncher, self).__init__()
        #main window properties
        self.setWindowTitle('Network Deployment Automation Maintenance Tool')
        self.setWindowIcon(QIcon('images/icon.ico'))
        self.setFixedSize(900, 700)
        self.closeEvent = self.closeEvent
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)

        #global UI widgets
        self.launcher = QWidget()
        self.deployment = QWidget()
        self.settings = QWidget()
        self.troubleshooting = QWidget()
        self.monitoring = QWidget()

        #keep track of any threads during runtime, avoid cleanup
        self.threads = []

        #Set up stack of UI
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.launcher)
        self.Stack.addWidget(self.deployment)
        self.Stack.addWidget(self.settings)
        self.Stack.addWidget(self.troubleshooting)
        self.Stack.addWidget(self.monitoring)

        #set the main window to the stack
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.Stack)

        #set window style and layout
        self.setStyleSheet(DEFAULT_STYLE)
        self.setLayout(mainLayout)

        # check if settings file is setup
        if not os.path.isfile('./Settings.xml'):
            self.notSetup = True
            self.Stack.setCurrentIndex(2) #if it's not send them to settings page
        else:
            self.notSetup = False
            self.Stack.setCurrentIndex(0) #if there is a file we put them in the launcher

        loginNotAccessed = True

        #setup the managers for passwords and the login itself
        self.passwordManager = PasswordManager()
        self.loginManager = LoginManager(self.passwordManager)

        # get Passwords Required For Functionality
        if not self.notSetup:
            self.loginManager.getPasswordsAlert()
            loginNotAccessed = False #show that we've entered the login page

        # We have the passwords and we're ready to launch the application
        if not self.notSetup and self.loginManager.passwordsEntered:

            #initialize Module Classes
            self.monitoringModule = MaintenanceModule(self, self.monitoring)
            self.deploymentModule = DeploymentModule(self, self.deployment)
            self.troubleshootingModule = TroubleshootingModule(self,self.troubleshooting)
            self.settingsModule = SettingsModule(self,self.settings)

            #appropriate UI layouts and methods
            self.launcherUI()
            self.settingsModule.settingsUI(self)
            self.troubleshootingModule.troubleshootingUI(self)
            self.deploymentModule.deploymentUI(self)
            self.monitoringModule.maintenanceUI(self)

            #finally show it all
            self.show()

        # if they haven't set up the programme at all load some of the modules
        elif (self.notSetup and loginNotAccessed) or self.loginManager.wantsSettings:
            # initialize Module Classes
            self.monitoringModule = MaintenanceModule(self, self.monitoring)
            self.deploymentModule = DeploymentModule(self, self.deployment)
            self.troubleshootingModule = TroubleshootingModule(self, self.troubleshooting)
            self.settingsModule = SettingsModule(self, self.settings)

            # appropriate UI layouts and methods for settings module
            self.settingsModule.settingsUI(self)

            # if they've clicked the edit settings button on the login page
            if self.loginManager.wantsSettings:
                self.notSetup = True
                self.Stack.setCurrentIndex(2)

            # show the modules loaded
            self.show()
        else:
            #if we don't have the correct passwords then we close
            sys.exit()

    # Generate the GUI for the launcher window
    def launcherUI(self):

        verticalContainer = QVBoxLayout()

        settingsLayout = QHBoxLayout()
        settingsLayout.setContentsMargins(0,0,0,135)
        settingsLayout.addStretch()
        settingsButton = ImageButton(QPixmap("images/settings.png"))
        settingsButton.setWhatsThis("Change your settings for the application at any time here")
        settingsButton.clicked.connect(self.initialiseSettings)
        settingsLayout.addWidget(settingsButton)
        verticalContainer.addLayout(settingsLayout)

        gridLayout = QGridLayout()
        deploymentButton = ImageButton(QPixmap("images/deployment.png"))
        deploymentButton.setWhatsThis("This module is used to set up devices for deployment")
        deploymentButton.clicked.connect(self.initialiseDeployment)
        gridLayout.addWidget(deploymentButton, 0, 0, 1, 1)
        monitoringButton = ImageButton(QPixmap("images/monitoring.png"))
        monitoringButton.setWhatsThis("Keep track of any changes made to configurations on devices you've deployed with this app")
        monitoringButton.clicked.connect(self.initialiseMonitoring)
        gridLayout.addWidget(monitoringButton, 0, 1, 1, 1)
        troubleshootingButton = ImageButton(QPixmap("images/troubleshooting.png"))
        troubleshootingButton.setWhatsThis("This module is used to scan a network & interface with live devices")
        troubleshootingButton.clicked.connect(self.initialiseTroubleshooting)
        gridLayout.addWidget(troubleshootingButton, 0, 2, 1, 1)

        verticalContainer.addLayout(gridLayout)
        verticalContainer.addStretch()

        self.launcher.setLayout(verticalContainer)

    # --- Initialise the mian application windows ---
    def initialiseLauncher(self):
        if not os.path.isfile('./Settings.xml') or self.loginManager.wantsSettings:
            QMessageBox.information(self, "Settings", "You must fill in the information required to use this application")
        else:
            self.Stack.setCurrentIndex(0)

    def initialiseDeployment(self):
        self.Stack.setCurrentIndex(1)

    def initialiseMonitoring(self):
        self.Stack.setCurrentIndex(4)

    def initialiseTroubleshooting(self):
        self.Stack.setCurrentIndex(3)

    def initialiseSettings(self):
        self.Stack.setCurrentIndex(2)

    # Handle exit events and clean up files
    def closeEvent(self, event):
        global restartRequired
        # Below checks are to see if we're not actually in the main app
        pressedXAtLogin = not self.notSetup and not self.loginManager.passwordsEntered
        if self.settingsModule.restart:
            restartRequired = True
        if self.loginManager.wantsSettings:  # check if we clicked edit settings on the login window
            event.accept()
        elif pressedXAtLogin:  # check if we're at the login window
            event.accept()
        elif self.notSetup: # check if we are at the initial settings screen
            event.accept()
        else:
            #check if they're deploying devices, this is important to know in case they stop deploying mid way
            exitMsg = "Are you sure you want to quit?"
            if self.deploymentModule.blocked:
                exitMsg = "You're currently deploying devices, If you quit now you could damage your equipment. Are you sure?"

            reply = QMessageBox.question(self, 'Closing Application',exitMsg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

# Min application method
if __name__ == '__main__':
    global restartRequired
    restartRequired = True
    app = QApplication(sys.argv)
    while restartRequired:
        restartRequired = False
        ex = windowLauncher()
        app.exec_()