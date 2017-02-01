import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


import scanner
import os.path
from imagebutton import ImageButton
import messagewindow as msg

class TroubleshootingModule:
    def __init__(self, window, layout):
        self.window = window
        self.layout = layout
        self.blocked = False
        self.threads = []

    def troubleshootingUI(self,window):
        try:
            verticalContainer = QVBoxLayout(window)
            verticalContainer.setObjectName("verticalContainer")

            topBarLayout = QHBoxLayout(window)
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
            innerContainer = QHBoxLayout(window)
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
            loginButton.clicked.connect(self.loginToDevice)
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

            mapContainer = QVBoxLayout(window)
            dir_path = os.path.dirname(os.path.realpath(__file__))
            self.image = QLabel()
            blankImage = QPixmap(551,416)
            blankImage.fill(Qt.white)
            mapImage = QPixmap(blankImage)
            mapImage = mapImage.scaled(mapImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image.setPixmap(mapImage)
            self.image.setStyleSheet("background-color: white")
            self.image.mousePressEvent = self.getPos
            mapContainer.addWidget(self.image)
            self.scannerProgressBar = QProgressBar(window)
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

            self.layout.setLayout(verticalContainer)
        except Exception as e: print(str(e))

    def refreshPage(self):
        if(self.blocked):
            msg.messageWindow("Process is currently running","Cannot refresh page while scanning network",False)
        else:
            #clear fields and progress bar
            self.scannerProgressBar.setValue(0)
            self.deviceAddress.setText("")
            self.deviceUsername.setText("")
            self.devicePassword.setText("")

            #clear image
            blankImage = QPixmap(551, 416)
            blankImage.fill(Qt.white)
            mapImage = QPixmap(blankImage)
            mapImage = mapImage.scaled(mapImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image.setPixmap(mapImage)

    # get mouse position from click event
    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(str(x) + " " + str(y))


    # update the network map image with a new scan
    def displayImage(self):
        try:
            if not self.blocked:
                self.blocked = True
                thread = NetworkScanner(self.window)
                thread.trigger.connect(self.updateScannerProgress)
                thread.setup(1)
                thread.start()
                self.threads.append(thread)
            else:
                QMessageBox.information(self, "Scan Running", "You're already running a network scan")
        except Exception as e: print(str(e))

    def loginToDevice(self):
        print("login")


    # called from thread, updates the progress bar or wraps up and sets new image
    def updateScannerProgress(self, percentage):
        try:
            if (percentage == 101):
                G = scanner.graphLocation
                nx.draw_networkx(G)
                plt.axis('off')
                plt.autoscale()
                plt.savefig("network_path.png", bbox_inches='tight')  # save as png

                dir_path = os.path.dirname(os.path.realpath(__file__))
                mapImage = QPixmap(dir_path + '\\network_path.png')
                mapImage = mapImage.scaled(mapImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image.setPixmap(mapImage)
                self.blocked = False
                self.scannerProgressBar.setValue(0)
                self.threads.clear()
            else:
                self.scannerProgressBar.setValue(percentage)
        except Exception as e: print(str(e))

class NetworkScanner(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(NetworkScanner, self).__init__(parent)

    def setup(self, thread_no):
        self.thread_no = thread_no

    def run(self):
        scanner.scanNetwork(self)