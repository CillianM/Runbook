import unittest
import sys

import secondaryWindows
from secondaryWindows import *
from deployment import getDatabaseListing

'''
...
----------------------------------------------------------------------
Ran 3 tests in 6.906s

OK
'''

class secondaryWindowsTesting(unittest.TestCase):

    def test_exportToCSV(self):
        exportToCSV()  #method requires CSV data from displayDatabasewindow so we expect and error
        secondaryWindows.csvData = 2  # insert wrong format of data
        exportToCSV()
        secondaryWindows.csvData = None  # insert wrong format of data
        exportToCSV()

    def test_messageWindow(self):
        messageWindow("Test","Test Description",False)
        messageWindow("Test", "Test Description", True)

    def test_databaseDisplay(self):
        #expect an exception with no proper data being passed in
        with self.assertRaises(Exception):
            displayDatabaseWindow("")

        listing = getDatabaseListing("password")
        displayDatabaseWindow(listing)

# class to actually run the QT window
class WindowRunner(QWidget):
    def __init__(self):
        super(WindowRunner,self).__init__()
        unittest.main() # run the tests after the window has closed


if __name__ == '__main__':
    app = QApplication(sys.argv)
    runner = WindowRunner()