import datetime
import random
import sys
import threading

import time
import os.path

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ftplib import *

from deployment import DeploymentModule
from troubleshooting import TroubleshootingModule
from settings import SettingsModule
from imagebutton import ImageButton

#Styling for progress bar
DEFAULT_STYLE = """

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
        deploymentModule = DeploymentModule(self, self.deployment)
        troubleshootingModule = TroubleshootingModule(self,self.troubleshooting)
        settingsModule = SettingsModule(self,self.settings)

        #appropriate UI layouts and methods
        self.launcherUI()
        settingsModule.settingsUI(self)
        troubleshootingModule.troubleshootingUI(self)
        deploymentModule.deploymentUI(self)

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

#handle exit events and clean up files
def exitHandler():
    os.remove("network_path.png")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(exitHandler) #connect app to handler to remove files not needed outside runtime
    ex = windowLauncher()
    sys.exit(app.exec_())

