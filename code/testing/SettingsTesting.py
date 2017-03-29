import unittest
import sys

from settings import *

from PyQt5.QtWidgets import *

'''
----------------------------------------------------------------------
Ran 6 tests in 4.093s

OK
'''

settings = None
window = None

class SettingsTesting(unittest.TestCase):
    global settings,window
    def test_UI(self):
        window.windowMaker()

    def test_fillSettingsFields(self):
        settings.fillSettingsFields()

    def test_allSettingsFieldsFilled(self):
        self.assertTrue(settings.allSettingsFieldsFilled())

    def test_applySettings(self):
        settings.applySettings()
        window.notSetup = True
        settings.applySettings()

    def test_gets(self):
        self.assertEqual(getFtpAddress(),"localhost")
        self.assertEqual(getFtpUsername(), "user")
        self.assertEqual(getOsPath(), "/os/")
        self.assertEqual(getConfPath(), "/conf/")
        self.assertEqual(getIniConfPath(), "/iniconf/")
        self.assertEqual(getConsoleName(), "user")
        self.assertEqual(getConsoleAddress(), "localhost")
        self.assertEqual(getDatabaseAddress(), "localhost")
        self.assertEqual(getDatabaseUsername(), "user")
        self.assertEqual(getDatabaseTable(), "configurations")
        self.assertEqual(getDatabase(), "runbook")

    def test_makeLegalPath(self):
        self.assertEqual(settings.makeLegalPath("conf"), "/conf/")
        self.assertEqual(settings.makeLegalPath("/conf"), "/conf/")
        self.assertEqual(settings.makeLegalPath("conf/"), "/conf/")
        self.assertEqual(settings.makeLegalPath("/conf/"), "/conf/")


# class to actually run the QT window
class WindowRunner(QWidget):
    def __init__(self):
        super(WindowRunner,self).__init__()
        global settings,window
        self.notSetup = False
        window = self
        settings = SettingsModule(self,self)
        settings.settingsUI(self)
        unittest.main()

    def windowMaker(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Testing Settings Layout")
        self.dialog.setStyleSheet("background-color: rgb(69,90,100);")
        self.dialog.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        mainLayout = QVBoxLayout(self.dialog)

        mainLayout.addLayout(self.layout())

        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.dialog.exec_()

    def initialiseLauncher(self):
        print("launcher")

    def applySettings(self):
        print("settings applied")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    runner = WindowRunner()