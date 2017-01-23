from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog,QWidget

import connect_session

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1200, 933)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        MainWindow.setStyleSheet("background-color: rgb(69,90,100);")
        self.gridLayoutWidget.setGeometry(QtCore.QRect(127, -23, 900, 933))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.deploymentButton = ImageButton(QtGui.QPixmap("deployment.png"))
        self.deploymentButton.setObjectName("deploymentButton")
        self.deploymentButton.clicked.connect(self.initialiseDeployment)
        self.gridLayout.addWidget(self.deploymentButton, 0, 1, 1, 1)
        self.monitoringButton = ImageButton(QtGui.QPixmap("monitoring.png"))
        self.monitoringButton.setObjectName("pushButton")
        self.monitoringButton.clicked.connect(self.initialiseMonitoring)
        self.gridLayout.addWidget(self.monitoringButton, 0, 0, 1, 1)
        self.troubleshootingButton = ImageButton(QtGui.QPixmap("troubleshooting.png"))
        self.troubleshootingButton.setObjectName("pushButton_3")
        self.troubleshootingButton.clicked.connect(self.initialiseTroubleshooting)
        self.gridLayout.addWidget(self.troubleshootingButton, 0, 2, 1, 1)

        self.settingsButtonLayout = QtWidgets.QWidget(self.centralwidget)
        self.settingsButtonLayout.setGeometry(QtCore.QRect(1100, 0, 100, 100))
        self.settingsButtonLayout.setObjectName("settingsButtonLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.settingsButtonLayout)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.settingsButton = ImageButton(QtGui.QPixmap("settings.png"))
        self.settingsButton.setObjectName("settingsButton")
        self.settingsButton.clicked.connect(self.initialiseSettings)
        self.gridLayout_2.addWidget(self.settingsButton, 0, 0, 1, 1)

        self.retranslateUi(MainWindow)

    def initialiseDeployment(self):
            dialog = QDialog()
            dialog.ui = connect_session.Ui_ConnectSession()
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def initialiseMonitoring(self):
        print("Monitoring")

    def initialiseTroubleshooting(self):
        print("Troubleshooting Module")

    def initialiseSettings(self):
        print("Settings Screen")


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Launcher"))
        self.deploymentButton.setText(_translate("MainWindow", "Deployment Module"))
        self.monitoringButton.setText(_translate("MainWindow", "Monitoring Module"))
        self.troubleshootingButton.setText(_translate("MainWindow", "Troubleshooting Module"))
        self.settingsButton.setText(_translate("MainWindow", "Settings"))

class ImageButton(QtWidgets.QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(ImageButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = QDialog()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())