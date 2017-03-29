import unittest
import sys

from LoginManager import PasswordManager
from maintenance import *

window = None
maintenance = None

class MaintenanceTesting(unittest.TestCase):
    global window,maintenance
    def test_makeUI(self):
        maintenance.getFileHistory()
        window.windowMaker()

    def test_findLast(self):
        self.assertEqual(maintenance.findLast("helloh","h"),5)

    def test_historyGrabber(self):
        maintenance.startHistoryGrabber("C:\\Users\\Cillian\\Desktop\\file.conf")

    def test_grabber(self):
        maintenance.startGrabber()

    def test_sortTimestamps(self):
        list = ['08-03-2017 15:10:59.11','01-03-2017 00:11:47.09']
        self.assertEqual(maintenance.sortTimeStamps(list),['01-03-2017 00:11:47.09','08-03-2017 15:10:59.11'])

    def test_openExplorer(self):
        maintenance.openExplorer()

    def test_displayFile(self):
        maintenance.displayFile()

    def test_addToRepo(self):
        maintenance.selectedConfig.addItem("file")
        maintenance.fileToPush = "C:\\Users\\Cillian\\Desktop\\file.conf"
        maintenance.commitTitle.setText("Title")
        maintenance.commitDescription.setText("Title")
        maintenance.startPush()


# class to actually run the QT window
class WindowRunner(QWidget):
    def __init__(self):
        super(WindowRunner,self).__init__()
        global window,maintenance
        window = self
        self.passwordManager = PasswordManager()
        self.passwordManager.setDatabasePassword("password")
        self.passwordManager.setFtpPassword("password")
        maintenance = MaintenanceModule(self, self)
        maintenance.maintenanceUI(self)
        unittest.main()

    def windowMaker(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Testing Maintenance Layout")
        self.dialog.setStyleSheet("background-color: rgb(69,90,100);")
        self.dialog.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        mainLayout = QVBoxLayout(self.dialog)

        mainLayout.addLayout(self.layout())

        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.dialog.exec_()

    def initialiseLauncher(self):
        print("Launcher")

    def getFileHistory(self):
        print("History")

    def startPush(self):
        print("Push")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    runner = WindowRunner()