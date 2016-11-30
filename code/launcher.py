from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog,QWidget

import connect_session

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 800, 300))
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


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.deploymentButton.setText(_translate("MainWindow", "Deployment Module"))
        self.maintenenceButton.setText(_translate("MainWindow", "Maintenence Module"))
        self.troubleshootingButton.setText(_translate("MainWindow", "Troubleshooting Module"))

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