import networkx as nx
import matplotlib.pyplot as plt
import paramiko
import xmltodict

import deployment
import secondaryWindows
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as Toolbar

from Connectivity import patch_crypto_be_discovery, isJunosDevice
from customStyling import getTopBarLayout, IconLineEdit, ImageLable
from scanner import Scanner


class TroubleshootingModule:
    def __init__(self, window, layout):
        self.window = window
        self.layout = layout
        self.blocked = False
        self.statisticsText=None

        # Network map window variables
        self.figure = None
        self.canvas = None
        self.nodePositioning = None

        self.scanner = Scanner()

    # Creating the troubleshooting module GUI
    def troubleshootingUI(self, window):
        try:
            verticalContainer = QVBoxLayout()
            verticalContainer.setObjectName("verticalContainer")

            topBarLayout = getTopBarLayout(self, window)
            verticalContainer.addLayout(topBarLayout)

            innerContainer = QHBoxLayout()
            innerContainer.setContentsMargins(0, 0, 0, 0)
            innerContainer.setObjectName("innerContainer")

            loginHeadingLayout = QVBoxLayout()
            loginHeadingLayout.setSpacing(0)
            loginLabel = ImageLable('./images/hexagon.png', "Log Into a Device")
            loginLabel.setWhatsThis("Allows you to get more detailed information by logging into the device")
            loginLabel.setStyleSheet("background-color: rgb(0,188,212);border-top-left-radius: 10px;border-top-right-radius: 10px;font-size:16px;")
            loginHeadingLayout.addWidget(loginLabel.getWidget())

            detailsContainer = QVBoxLayout()
            loginContainer = QVBoxLayout()
            self.deviceAddress = IconLineEdit('./images/device.png', "Device Address",False)
            loginContainer.addWidget(self.deviceAddress.getWidget())
            self.deviceUsername = IconLineEdit('./images/user.png', "Device Username",False)
            loginContainer.addWidget(self.deviceUsername.getWidget())
            self.devicePassword = IconLineEdit('./images/key.png', "Device Password",True)
            loginContainer.addWidget(self.devicePassword.getWidget())
            loginButton = QPushButton("Connect to device")
            loginButton.setObjectName("deploymentButton")
            loginButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
            loginButton.clicked.connect(self.getHardwareDetails)
            loginContainer.addWidget(loginButton)

            loginFrame = QFrame()
            loginFrame.setLayout(loginContainer)
            loginFrame.setObjectName("loginFrame")
            loginFrame.setStyleSheet("QFrame#loginFrame {background-color: white; border-bottom-left-radius: 10px; border-bottom-right-radius: 10pxd}")
            loginHeadingLayout.addWidget(loginFrame)
            detailsContainer.addLayout(loginHeadingLayout)

            statisticsHeadingLayout = QVBoxLayout()
            statisticsHeadingLayout.setSpacing(0)
            statisticsLabel = ImageLable('./images/hexagon.png', "Network Statistics")
            statisticsLabel.setStyleSheet("background-color: rgb(0,188,212);border-top-left-radius: 10px;border-top-right-radius: 10px;font-size:16px;")
            statisticsHeadingLayout.addWidget(statisticsLabel.getWidget())

            statisticsContainer = QVBoxLayout()

            self.statisticsDetails = QTextEdit()
            self.statisticsDetails.setReadOnly(True)
            self.statisticsDetails.setText("When you log into a device or map the network, relevant information will appear here.")
            statisticsContainer.addWidget(self.statisticsDetails)

            statisticsFrame = QFrame()
            statisticsFrame.setLayout(statisticsContainer)
            statisticsFrame.setStyleSheet("background-color: white; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
            statisticsHeadingLayout.addWidget(statisticsFrame)
            detailsContainer.addLayout(statisticsHeadingLayout)
            innerContainer.addLayout(detailsContainer)

            mapContainer = QVBoxLayout()

            # use matplotlib bankends for pyqt
            self.figure = plt.figure()
            self.canvas = Canvas(self.figure)
            toolbar = Toolbar(self.canvas, self.window)
            self.canvas.mpl_connect('button_press_event', self.getPos)


            mapContainer.addWidget(toolbar)
            mapContainer.addWidget(self.canvas)
            self.scannerProgressBar = QProgressBar(window)
            self.scannerProgressBar.setProperty("value", 0)
            self.scannerProgressBar.setOrientation(Qt.Horizontal)
            self.scannerProgressBar.setTextVisible(False)
            self.scannerProgressBar.setObjectName("self.progressBar")
            self.scannerProgressBar.setStyleSheet("QProgressBar::chunk:horizontal { background-color: rgb(0,188,212)}")
            mapContainer.addWidget(self.scannerProgressBar)

            mappingButton = QPushButton("Start network mapping")
            mappingButton.setWhatsThis("Will scan your network and generate an image of it to be displayed above")
            mappingButton.setObjectName("deploymentButton")
            mappingButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
            mappingButton.clicked.connect(self.displayImage)
            mapContainer.addWidget(mappingButton)

            innerContainer.addLayout(mapContainer)
            verticalContainer.addLayout(innerContainer)

            self.layout.setLayout(verticalContainer)
        except Exception as e:
            print(str(e))

    # Refresh window
    def refreshPage(self):
        if self.blocked:
            secondaryWindows.messageWindow("Process is currently running", "Cannot refresh page while scanning network", False)
        else:
            # clear fields and progress bar
            self.scannerProgressBar.setValue(0)
            self.deviceAddress.setText("")
            self.deviceUsername.setText("")
            self.devicePassword.setText("")
            self.statisticsDetails.setText("When you log into a device it's details will appear here")

            # clear canvas
            self.canvas.figure.clf()
            self.canvas.draw()

    # Get mouse position from click event
    def getPos(self, event):
        try:
            # make sure we're looking in the window and positioning data is available
            if not (event.xdata is None or event.ydata is None) and not self.nodePositioning is None:
                # set gap around actual position to allow for mouse click
                gap = 0.1
                for key in self.nodePositioning:
                    currentDictEntry = self.nodePositioning[key]
                    currentKey = key
                    x = currentDictEntry[0]
                    y = currentDictEntry[1]
                    # if we fall within the gap of the current key then we're close to that key
                    if (-gap < x - event.xdata < gap) and (-gap < y - event.ydata < gap):
                        # check if we're looking at our ip address
                        myIp = self.scanner.getMyIpAddr()
                        if not currentKey == myIp:
                            currentKey = self.scanner.getMissingIpNumbers() + currentKey
                        macAddr = self.scanner.returnMacAddr(currentKey)

                        vendor = self.scanner.returnVendor(macAddr)
                        self.deviceAddress.setText(currentKey)
                        self.statisticsDetails.setText("IP Address: " + currentKey
                                                       + "\nMac Address: " + macAddr
                                                       + "\nVendor: " + vendor + "\n")
        except Exception as e:
            print(str(e))

    # Update the network map image with a new scan
    def displayImage(self):
        try:
            if not self.blocked:
                self.blocked = True
                thread = NetworkScanner(self.window)
                thread.setup(self.scanner)
                thread.trigger.connect(self.updateScannerProgress)
                thread.start()
            else:
                secondaryWindows.messageWindow("Scan Running", "You're already running a network scan", False)
        except Exception as e:
            print(str(e))

    # Called from thread, updates the progress bar or wraps up and sets new image
    def updateScannerProgress(self, percentage):
        if (percentage == -1):
            secondaryWindows.messageWindow("Error","Error Scanning Network",True)
            self.blocked = False
        else:
            try:
                if (percentage == 101):
                    networkGraph = self.scanner.getGraph()
                    self.nodePositioning = nx.spring_layout(networkGraph)  # set positioning so we can reference it later
                    nx.draw_networkx(networkGraph, self.nodePositioning, node_color='#00BCD4', node_size=500)
                    plt.axis('off')
                    self.figure = plt.figure()
                    self.canvas.draw()

                    self.blocked = False
                    self.scannerProgressBar.setValue(0)
                else:
                    self.scannerProgressBar.setValue(percentage)
            except Exception as e:
                print(str(e))

    # Get detailed information from a Juniper device on the network
    def getHardwareDetails(self):
        address = self.deviceAddress.text()
        username = self.deviceUsername.text()
        password = self.devicePassword.text()

        if (len(address) < 1 or len(username) < 1 or len(password) < 1):
            secondaryWindows.messageWindow("Empty Fields", "Please ensure all fields are filled", False)
            return

        thread = DeviceInfo(self.window)
        thread.trigger.connect(self.updateStatisticField)
        thread.setup(self, address, username, password)
        thread.start()
        #show we're connecting to the device
        self.statisticsDetails.append("\n Connecting to device...")

    # Add info to the device statistics field
    def updateStatisticField(self, code):
        if code==0:
            self.statisticsDetails.append("\n Connected!")
            self.statisticsDetails.append(self.statisticsText)
        elif code ==-1:
            self.statisticsDetails.append("\n Unsupported Device!")
            secondaryWindows.messageWindow("Unsupported Device",
                                           """Error getting data from device as it's not currently supported, Junos devices are currently the only
                                           ones supported""",
                                           True)
        else:
            secondaryWindows.messageWindow("Error", "Error getting data from the Juniper Device. Check input data and try again.", True)

# Parse the xml output form the Juniper device
def getStatusInfo(xml):
    try:
        xml = xml.split("<rpc-reply")[1]
        xml = "<rpc-reply" + xml
        xml = xml.split("</rpc-reply>")[0]
        xml += "</rpc-reply>"

        xmlDict = xmltodict.parse(xml)
        upTime = xmlDict['rpc-reply']['route-engine-information']['route-engine']['up-time']['#text']
        cpuTemp = xmlDict['rpc-reply']['route-engine-information']['route-engine']['cpu-temperature']['#text']
        #remove the F reafing form the string
        cpuTemp = cpuTemp.split("/")[0]
        memUtilised = xmlDict['rpc-reply']['route-engine-information']['route-engine']['memory-system-total-util']

        return "Uptime: " + upTime + "\nCpu Temp: " + cpuTemp + "\nMem Utilised: " + memUtilised + "%"
    except Exception as e:
        print("Error connecting to the database: " + str(e))

# Check if there are any current alarms on the device
def isAlarms(xml):
    try:
        xml = xml.split("<rpc-reply")[1]
        xml = "<rpc-reply" + xml
        xml = xml.split("</rpc-reply>")[0]
        xml += "</rpc-reply>"

        xmlDict = xmltodict.parse(xml)
        alarms=xmlDict['rpc-reply']['alarm-information']['alarm-summary']

        if "no-active-alarms" in alarms:
            return False
        else:
            return True
    except Exception as e:
        print("Error connecting to the database: " + str(e))

# Create a thread to scan the network
class NetworkScanner(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(NetworkScanner, self).__init__(parent)
        self.scanner = None

    def setup(self,scanner):
        self.scanner = scanner

    def run(self):
        self.scanner.scanNetwork(self)

# File grabber class to get files off UI thread
class DeviceInfo(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(DeviceInfo, self).__init__(parent)

    def setup(self, callingWindow, address, username, password):
        self.callingWindow = callingWindow
        self.address = address
        self.username = username
        self.password = password

    def run(self):
        try:
            returnedData = loginToDevice(self.callingWindow,self.address, self.username, self.password)
            if returnedData is "NOJUNOS":
                self.trigger.emit(-1)
            elif not returnedData is None:
                self.callingWindow.statisticsText = returnedData
                self.trigger.emit(0)
            else:
                self.trigger.emit(1)
        except:
            self.trigger.emit(1)

# Log into juniper device and pull down hardware information
def loginToDevice(callingWindow,address, username, password):

    patch_crypto_be_discovery()

    if isJunosDevice(address):
        try:
            #Log into the device
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(address, 22, username, password)
            term = ssh.invoke_shell()

            #Check if root is logging in
            if username=="root":
                deployment.send_command(term, "cli")

            #Gather data from the device
            deployment.send_command(term, "set cli screen-length 0")
            sysStatus = deployment.send_command(term, "show chassis routing-engine | display xml")
            alarms = deployment.send_command(term, "show chassis alarms | display xml")

            sysStatusData = getStatusInfo(sysStatus)
            alarm = isAlarms(alarms)

            ssh.close()

            macAddr = callingWindow.scanner.returnMacAddr(address)
            vendor = callingWindow.scanner.returnVendor(macAddr)

            basicDetails = ("IP Address: " + address
                                           + "\nMac Address: " + macAddr
                                           + "\nVendor: " + vendor + "\n")

            if alarm:
                sysStatusData += "\nALARM WARNING!"
            else:
                sysStatusData += "\nNo Alarms"

            return sysStatusData
        except:
            return None
    else:
        return "NOJUNOS"