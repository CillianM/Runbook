import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#Styling for progress bar
DEFAULT_STYLE = """

background-color: rgb(69,90,100);

}
"""


class windowLauncher(QWidget):
    def __init__(self):
        super(windowLauncher, self).__init__()

        self.launcher = QWidget()
        self.deployment = QWidget()
        self.stack3 = QWidget()

        self.launcherUI()
        self.deploymentUI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.launcher)
        self.Stack.addWidget(self.deployment)

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.Stack)

        self.setStyleSheet(DEFAULT_STYLE)
        self.setLayout(mainLayout)

        self.setFixedSize(900, 700)
        self.setWindowTitle('Network Deployment Automation Maintenance Tool')
        self.show()


    def launcherUI(self):

        verticalContainer = QVBoxLayout(self)

        settingsLayout = QHBoxLayout(self)
        settingsLayout.addSpacing(1000)
        settingsLayout.setContentsMargins(0,0,0,135)
        blankLabel = QLabel(self)
        settingsLayout.addWidget(blankLabel)
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

        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setObjectName("horizontalLayout")
        gridLayout_4 = QGridLayout()
        gridLayout_4.setObjectName("gridLayout_4")
        gridLayout_4.setVerticalSpacing(60)
        gridLayout_7 = QGridLayout()
        gridLayout_7.setObjectName("gridLayout_7")
        label = QLabel("   TO   ")
        label.setObjectName("label")
        label.setStyleSheet("color:white; font-size:16px;")
        gridLayout_7.addWidget(label, 0, 1, 1, 1)
        lineEdit = QLineEdit(self)
        lineEdit.setObjectName("lineEdit")
        lineEdit.setStyleSheet("background-color: rgb(255,255,255);")
        lineEdit.setPlaceholderText("> Port")
        gridLayout_7.addWidget(lineEdit, 0, 0, 1, 1)
        lineEdit_2 = QLineEdit(self)
        lineEdit_2.setObjectName("lineEdit_2")
        lineEdit_2.setStyleSheet("background-color: rgb(255,255,255);")
        lineEdit_2.setPlaceholderText(">> Port")
        gridLayout_7.addWidget(lineEdit_2, 0, 2, 1, 1)
        gridLayout_4.addLayout(gridLayout_7, 1, 0, 1, 1)
        formLayout = QVBoxLayout()
        formLayout.setObjectName("formLayout")
        checkBox = QCheckBox("Clone to Backup Partition")
        checkBox.setObjectName("checkBox")
        checkBox.setStyleSheet("color:white; font-size:16px;")
        formLayout.addWidget(checkBox)
        gridLayout_4.addLayout(formLayout, 3, 0, 1, 1)
        pushButton_2 = QPushButton("Begin Deployment")
        pushButton_2.setObjectName("pushButton_2")
        pushButton_2.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
        gridLayout_4.addWidget(pushButton_2, 5, 0, 1, 1)
        lineEdit_3 = QLineEdit(self)
        lineEdit_3.setPlaceholderText("Password")
        lineEdit_3.setEchoMode(QLineEdit.Password)
        lineEdit_3.setStyleSheet("background-color: rgb(255,255,255);")
        lineEdit_3.setObjectName("lineEdit_3")
        gridLayout_4.addWidget(lineEdit_3, 2, 0, 1, 1)
        comboBox = QComboBox(self)
        comboBox.setObjectName("comboBox")
        comboBox.setStyleSheet("background-color: rgb(255,255,255);")
        gridLayout_4.addWidget(comboBox, 0, 0, 1, 1)
        formLayout_2 = QVBoxLayout()
        formLayout_2.setObjectName("formLayout_2")
        formLayout_2.setSpacing(10)
        label_3 = QLabel("Inital Configuration Range(Optional)")
        label_3.setObjectName("label_3")
        label_3.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
        formLayout_2.addWidget(label_3)
        comboBox_2 = QComboBox(self)
        comboBox_2.setObjectName("comboBox_2")
        comboBox_2.setStyleSheet("background-color: rgb(255,255,255);")
        formLayout_2.addWidget(comboBox_2)
        comboBox_3 = QComboBox(self)
        comboBox_3.setObjectName("comboBox_3")
        comboBox_3.setStyleSheet("background-color: rgb(255,255,255);")
        formLayout_2.addWidget(comboBox_3)
        gridLayout_4.addLayout(formLayout_2, 4, 0, 1, 1)
        gridLayout_4.setRowStretch(0, 1)
        gridLayout_4.setRowStretch(1, 2)
        gridLayout_4.setRowStretch(2, 2)
        gridLayout_4.setRowStretch(3, 1)
        gridLayout_4.setRowStretch(4, 1)
        gridLayout_4.setRowStretch(5, 2)
        horizontalLayout.addLayout(gridLayout_4)

        gridLayout_5 = QGridLayout()
        gridLayout_5.setObjectName("gridLayout_5")
        progressBar = QProgressBar(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(progressBar.sizePolicy().hasHeightForWidth())
        progressBar.setSizePolicy(sizePolicy)
        progressBar.setProperty("value", 24)
        progressBar.setOrientation(Qt.Vertical)
        progressBar.setInvertedAppearance(True)
        progressBar.setTextDirection(QProgressBar.TopToBottom)
        progressBar.setObjectName("progressBar")
        gridLayout_5.addWidget(progressBar, 0, 0, 1, 1)
        gridLayout_5.setContentsMargins(100, 0, 100, 0)
        horizontalLayout.addLayout(gridLayout_5)
        gridLayout_6 = QGridLayout()
        gridLayout_6.setObjectName("gridLayout_6")
        label_7 = QLabel("Deployment Progress")
        label_7.setObjectName("label_7")
        label_7.setStyleSheet("background-color: rgb(0,188,212); border: 1px solid black; font-size:16px;")
        gridLayout_6.addWidget(label_7, 1, 0, 1, 1)
        label_4 = QLabel("Connect to the device")
        label_4.setObjectName("label_4")
        label_4.setStyleSheet("color:white; font-size:16px;")
        gridLayout_6.addWidget(label_4, 2, 0, 1, 1)
        label_6 = QLabel("Log in")
        label_6.setObjectName("label_6")
        label_6.setStyleSheet("color:white; font-size:16px;")
        gridLayout_6.addWidget(label_6, 3, 0, 1, 1)
        label_5 = QLabel("Downloading OS")
        label_5.setObjectName("label_5")
        label_5.setStyleSheet("color:white; font-size:16px;")
        gridLayout_6.addWidget(label_5, 4, 0, 1, 1)
        label_10 = QLabel("Installing OS")
        label_10.setObjectName("label_10")
        label_10.setStyleSheet("color:white; font-size:16px;")
        gridLayout_6.addWidget(label_10, 5, 0, 1, 1)
        label_9 = QLabel("Rebooting the device")
        label_9.setObjectName("label_9")
        label_9.setStyleSheet("color:white; font-size:16px;")
        gridLayout_6.addWidget(label_9, 6, 0, 1, 1)
        label_8 = QLabel("Logging into the device")
        label_8.setObjectName("label_8")
        label_8.setStyleSheet("color:white; font-size:16px;")
        gridLayout_6.addWidget(label_8, 7, 0, 1, 1)
        label_11 = QLabel("Applying the configuration file")
        label_11.setObjectName("label_11")
        label_11.setStyleSheet("color:white; font-size:16px;")
        gridLayout_6.addWidget(label_11, 8, 0, 1, 1)
        label_12 = QLabel("Rebooting the device")
        label_12.setObjectName("label_12")
        label_12.setStyleSheet("color:white; font-size:16px;")
        gridLayout_6.addWidget(label_12, 9, 0, 1, 1)
        label_13 = QLabel("Deployment Successful")
        label_13.setObjectName("label_13")
        label_13.setStyleSheet("color:white; font-size:16px;")
        gridLayout_6.addWidget(label_13, 10, 0, 1, 1)
        horizontalLayout.addLayout(gridLayout_6)
        verticalContainer.addLayout(horizontalLayout)
        verticalContainer.addStretch()

        self.deployment.setLayout(verticalContainer)

    def initialiseLauncher(self):
        self.Stack.setCurrentIndex(0)
    def initialiseDeployment(self):
        self.Stack.setCurrentIndex(1)
    def initialiseMonitoring(self):
        print("Monitoring Module")
    def initialiseTroubleshooting(self):
        print("Troubleshooting Module")
    def initialiseSettings(self):
        print("Settings Menu")
    def refreshPage(self):
        print("Refresh")

    def display(self, i):
        self.Stack.setCurrentIndex(i)


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