import unittest
import sys

from LoginManager import *

'''
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK



'''


# global managers to point to
passwordManagerOne = PasswordManager()
loginManagerOne = LoginManager(passwordManagerOne)

passwordManagerTwo = PasswordManager()
loginManagerTwo = LoginManager(passwordManagerTwo)

passwordManagerThree = PasswordManager()
loginManagerThree = LoginManager(passwordManagerThree)

class LoginManagerTest(unittest.TestCase):
    global loginManagerOne, loginManagerTwo, loginManagerThree, passwordManagerOne, passwordManagerTwo, passwordManagerThree

    def test_gettingPasswords(self):
        # test successful connection
        self.assertEqual(passwordManagerOne.getDatabasePassword(),"password")
        self.assertEqual(passwordManagerOne.getFtpPassword(),"password")
        self.assertTrue(loginManagerOne.passwordsEntered)

        # test unsuccessful connection/ quitting out
        self.assertEqual(passwordManagerTwo.getDatabasePassword(), None)
        self.assertEqual(passwordManagerTwo.getFtpPassword(), None)

        # test asking for settings
        self.assertEqual(passwordManagerThree.getDatabasePassword(), None)
        self.assertEqual(passwordManagerThree.getFtpPassword(), None)

    def test_wantsSettings(self):
        self.assertFalse(loginManagerOne.wantsSettings)
        self.assertFalse(loginManagerTwo.wantsSettings)
        self.assertTrue(loginManagerThree.wantsSettings)

# class to actually run the QT window
class WindowRunner(QWidget):
    def __init__(self):
        super(WindowRunner,self).__init__()

        self.runWindow(1)
        self.runWindow(2)
        self.runWindow(3)

        unittest.main() # run the tests after the window has closed

    def runWindow(self,code):
        global loginManagerOne, loginManagerTwo, loginManagerThree
        if code == 1:
            loginManagerOne.getPasswordsAlert()
        if code == 2:
            loginManagerTwo.getPasswordsAlert()
        if code == 3:
            loginManagerThree.getPasswordsAlert()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    runner = WindowRunner()