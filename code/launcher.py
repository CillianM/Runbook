
import sys
import os.path

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from deployment import DeploymentModule
from troubleshooting import TroubleshootingModule
from settings import SettingsModule
from imagebutton import ImageButton

#Styling for progress bar
DEFAULT_STYLE = """
QWidget {
background-color: rgb(69,90,100);
}


"""
class windowLauncher(QWidget):
    def __init__(self):
        super(windowLauncher, self).__init__()
        #main window properties
        self.setWindowTitle('Network Deployment Automation Maintenance Tool')
        self.setWindowIcon(QIcon('icon.ico'))
        self.setFixedSize(900, 700)
        self.closeEvent = self.closeEvent

        #global UI widgets
        self.launcher = QWidget()
        self.deployment = QWidget()
        self.settings = QWidget()
        self.troubleshooting = QWidget()

        #keep track of any threads during runtime, avoid cleanup
        self.threads = []

        #Set up stack of UI
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.launcher)
        self.Stack.addWidget(self.deployment)
        self.Stack.addWidget(self.settings)
        self.Stack.addWidget(self.troubleshooting)

        #set the main window to the stack
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.Stack)

        #set window style and layout
        self.setStyleSheet(DEFAULT_STYLE)
        self.setLayout(mainLayout)

        # check if settings file is setup
        if not os.path.isfile('./Settings.xml'):
            self.Stack.setCurrentIndex(2) #if it's not send them to settings page
        else:
            self.Stack.setCurrentIndex(0) #if there is a file we put them in the launcher

        #initialize Module Classes
        self.deploymentModule = DeploymentModule(self, self.deployment)
        self.troubleshootingModule = TroubleshootingModule(self,self.troubleshooting)
        self.settingsModule = SettingsModule(self,self.settings)

        #appropriate UI layouts and methods
        self.launcherUI()
        self.settingsModule.settingsUI(self)
        self.troubleshootingModule.troubleshootingUI(self)
        self.deploymentModule.deploymentUI(self)

        #finally show it all
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

    # handle exit events and clean up files
    def closeEvent(self, event):
        #check if they're deploying devices, this is important to know in case they stop deploying mid way
        exitMsg = "Are you sure you want to quit?"
        if self.deploymentModule.blocked:
            exitMsg = "You're currently deploying devices, If you quit now you could damage your equipment. Are you sure?"

        reply = QMessageBox.question(self, 'Closing Application',exitMsg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if os.path.isfile('network_path.png'):
                os.remove("network_path.png") #remove files not needed outside runtime
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = windowLauncher()
    sys.exit(app.exec_())

