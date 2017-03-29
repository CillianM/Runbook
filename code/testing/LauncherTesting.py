import unittest
import sys

from launcher import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # run with no settings screen
    ex = windowLauncher()
    app.exec_()
    # run with x at login
    ex = windowLauncher()
    app.exec_()
    # run with x at login at settings
    ex = windowLauncher()
    app.exec_()
    # run with settings screen
    ex = windowLauncher()
    app.exec_()

