from datetime import datetime
from ftplib import FTP
from io import StringIO

import pymysql
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import secondaryWindows
from customStyling import IconLineEdit,getTopBarLayout, getComboxboxStyle, getVerticalScrollStyle, \
    getHorizontalScrollStyle
from secondaryWindows import messageWindow
from settings import getFtpAddress,\
    getDatabaseAddress,\
    getDatabaseUsername,\
    getConfPath, \
    getFtpUsername, \
    getDatabaseTable,\
    getDatabase

# Version Control for configuration files
class MaintenanceModule:
    def __init__(self, window, layout):
        self.window = window
        self.layout = layout
        self.blocked = False
        self.fileToPush = None
        self.pulledFilesContents = None
        self.fileToPull = None

        self.canUseCombobox = False  # ensures combo box doesn't fire when not wanted

        self.confFiles = None
        self.currentFilesHistory = None
        self.dots = []
        self.filesLinkedToDots = []
        self.ftpPassword = window.passwordManager.getFtpPassword()
        self.databasePassword = window.passwordManager.getDatabasePassword()

        self.changed = None
        self.removed = None

    # Creating the maintenance window GUI
    def maintenanceUI(self, window):
        try:
            verticalContainer = QVBoxLayout()
            verticalContainer.setObjectName("verticalContainer")

            #layout for top bar
            topBarLayout = getTopBarLayout(self,window)
            verticalContainer.addLayout(topBarLayout)

            innerContainerFrame = QFrame()
            innerContainer = QHBoxLayout()

            #layout for login detail section
            commitDetailsLayout = QVBoxLayout()
            commitDetailsFrame = QFrame()
            self.openFileButton = QPushButton("Select File")
            self.openFileButton.setWhatsThis("Select the file you're going to compare/push")
            self.openFileButton.setObjectName("openFile")
            self.openFileButton.setStyleSheet("background-color: rgb(255,255,255); font-size:16px;")
            self.openFileButton.clicked.connect(self.openExplorer)
            commitDetailsLayout.addWidget(self.openFileButton)

            #spacing
            spacing = QLabel()
            spacing.setText("")
            spacing.setStyleSheet("background-color: rgb(96,125,139); border: 1px solid rgb(96,125,139);")
            commitDetailsLayout.addWidget(spacing)

            self.commitTitle = IconLineEdit('./images/file.png',"Commit Title",False)
            self.commitTitle.setWhatsThis("Choose a suitable title to give to the commit you're making")
            commitDetailsLayout.addWidget(self.commitTitle.getWidget())
            self.commitDescription = QTextEdit()
            self.commitDescription.setWhatsThis("Choose a suitable description to give to the commit you're making")
            self.commitDescription.setPlaceholderText("Commit Description...")
            self.commitDescription.setStyleSheet("background-color: rgb(255,255,255); font-size:16px;")
            commitDetailsLayout.addWidget(self.commitDescription)
            addToRepoButton = QPushButton("Add to Repository")
            addToRepoButton.setObjectName("openFile")
            addToRepoButton.setWhatsThis("Click this to push the file you selected to the chosen timeline")
            addToRepoButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
            addToRepoButton.clicked.connect(self.startPush)
            commitDetailsLayout.addWidget(addToRepoButton)

            commitDetailsFrame.setFixedWidth(200)
            commitDetailsFrame.setStyleSheet("border: 1px solid rgb(96,125,139);")
            commitDetailsFrame.setLayout(commitDetailsLayout)
            innerContainer.addWidget(commitDetailsFrame)

            #bar to seperate 2 side
            lineLayout = QVBoxLayout()
            lineFrame = QFrame()
            lineFrame.setLayout(lineLayout)
            lineFrame.setStyleSheet("background-color: rgb(0,188,212); border: 1px solid rgb(96,125,139);")
            lineFrame.setFixedWidth(10)
            innerContainer.addWidget(lineFrame)

            #Config comparison layout
            configLayout = QVBoxLayout()


            self.selectedConfig = QComboBox()
            self.selectedConfig.setWhatsThis("This is a list of all the configs made to the devices you've deployed on this application")
            self.selectedConfig.setStyleSheet(getComboxboxStyle())
            self.selectedConfig.activated.connect(self.getFileHistory)
            configLayout.addWidget(self.selectedConfig)
            self.startGrabber() #grab files from database

            self.whatsAdded = QTextEdit()
            self.whatsAdded.setWhatsThis("This will show you what has been added to the file you've selected compared to what's on record")
            self.whatsAdded.setPlaceholderText("What's been added")
            self.whatsAdded.setReadOnly(True)
            self.whatsAdded.setStyleSheet("QTextEdit {background-color: rgb(255,255,255); font-size:16px; color:green}" + getVerticalScrollStyle())
            configLayout.addWidget(self.whatsAdded)
            self.whatsRemoved = QTextEdit()
            self.whatsRemoved.setWhatsThis("This will show you what has been removed from the file that's on record")
            self.whatsRemoved.setPlaceholderText("What's been removed")
            self.whatsRemoved.setReadOnly(True)
            self.whatsRemoved.setStyleSheet("QTextEdit {background-color: rgb(255,255,255); font-size:16px; color:red}" + getVerticalScrollStyle())
            configLayout.addWidget(self.whatsRemoved)
            innerContainer.addLayout(configLayout)

            # Commit dot layout
            commitDotHeadingFrame = QFrame()
            commitDotHeadingFrame.setFixedWidth(250)
            commitDotHeadingFrame.setStyleSheet("border: 1px solid rgb(96,125,139);")
            commitDotHeading = QVBoxLayout()
            commitDotHeading.setContentsMargins(0, 0, 0, 0)
            commitDotHeading.setSpacing(0)
            heading = QLabel()
            heading.setText("Commits")
            heading.setWhatsThis("This will list out the timeline of commits made to files over time")
            heading.setStyleSheet("background-color: rgb(0,188,212); font-size:12px;")
            commitDotHeading.addWidget(heading)

            self.commitDotLayout = QVBoxLayout()

            dot = QRadioButton()
            dot.setText("Commits Appear Here")
            dot.setStyleSheet("border: 1px solid rgb(96,125,139);")
            self.commitDotLayout.addWidget(dot)
            self.dots.append(dot)

            self.commitDotFrame = QFrame()
            self.commitDotFrame.setFixedWidth(230)
            self.commitDotFrame.setContentsMargins(0, 0, 0, 0)
            self.commitDotFrame.setStyleSheet("border: 1px solid rgb(96,125,139);")
            self.commitDotFrame.setLayout(self.commitDotLayout)

            self.scrollArea = QScrollArea()
            self.scrollArea.setWidget(self.commitDotFrame)
            self.scrollArea.setStyleSheet(getHorizontalScrollStyle() + getVerticalScrollStyle())

            commitDotHeading.addWidget(self.scrollArea)
            commitDotHeadingFrame.setLayout(commitDotHeading)
            innerContainer.addWidget(commitDotHeadingFrame)

            #entire inner window file config to layout
            innerContainerFrame.setLayout(innerContainer)
            innerContainerFrame.setStyleSheet("background-color: rgb(96,125,139); border: 1px solid black; font-size:16px; ")
            innerContainerEffect = QGraphicsDropShadowEffect()
            innerContainerEffect.setBlurRadius(15)
            innerContainerFrame.setGraphicsEffect(innerContainerEffect)

            verticalContainer.addWidget(innerContainerFrame)
            self.layout.setLayout(verticalContainer)
            self.canUseCombobox = True

            self.getFileHistory()


        except Exception as e:
            print(str(e))

    def findLast(self,s, ch):
        #builds a list of all the occurences of a character
        list =  [index for index, currentChar in enumerate(s) if currentChar == ch]
        #returns the last index
        return list[-1]

    # Pull file information form the database & start file comparing
    def displayFile(self):
        try:
            if not self.currentFilesHistory is None:
                timestampText = ""
                for i in range(len(self.dots)):
                    if self.dots[i].isChecked():
                        timestampText = self.dots[i].text()
                if not "Commit" in timestampText:
                    if not self.fileToPush is None:
                        path = self.currentFilesHistory[timestampText]
                        self.fileToPull = path
                        # thread to compare files
                        thread = FileComparer(self.window)
                        thread.setup(self)
                        thread.trigger.connect(self.updateChanges)
                        thread.start()
                    else:
                        secondaryWindows.messageWindow("Select File", "Please select a file first to compare them",False)
        except Exception as e:
            print(str(e))

    # Get file timestamps and the FTP path
    def getFileHistory(self):
        if self.canUseCombobox:
            if not self.confFiles is None:
                nameList = list(self.confFiles.keys())
                nameList.sort()
                self.startHistoryGrabber(nameList[self.selectedConfig.currentIndex()])

    # Compares two configuration files
    def compareFiles(self):
        if self.canUseCombobox:
            self.getContentsOfFile()  # first get the contents of the selected file
            if self.fileToPush is None:
                secondaryWindows.messageWindow("No local file selected","Need a local file to compare against",False)
                return
            else:
                try:
                    '''
                    every line that changes means another has been removed
                    we go through both files and compare them, keeping track
                    of line numbers as we go for readibility
                    '''
                    changed = []
                    removed = []
                    currentFile = self.pulledFilesContents.split("\n")
                    newFile = self.fileToPush
                    lineCount = 1
                    with open(newFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip("\n")
                            line = line.replace("\\\\", "")
                            if len(currentFile) > 1:
                                for i in range(0,len(currentFile)):
                                    if not line == currentFile[i]:
                                        changed.append("@" + str(lineCount) + ": " + line)
                                        removed.append("@" + str(lineCount) + ": " + currentFile[i])
                                        del currentFile[i]
                                        break
                                    else:
                                        del currentFile[i]
                                        break
                            else:
                                changed.append("@" + str(lineCount) + ": " + line)
                            lineCount += 1

                    if len(currentFile) > 1:
                        for i in range(0, len(currentFile)):
                            removed.append("@" + str(lineCount) + ": " + currentFile[i])
                            lineCount += 1

                    # go through and make sure it's not just moved to another line
                    if len(changed) > 1 and len(removed) > 1:
                        i = 0
                        while i < len(changed):
                            line = changed[i]
                            if len(line) > 1:
                                start = line.index(":")
                                line = line[start+2:]
                            for j in range(0,len(removed)):
                                if line in removed[j]:
                                    del changed[i]
                                    del removed[j]
                                    i -= 1
                                    break
                            i +=1

                    self.changed = changed
                    self.removed = removed
                except Exception as e:
                    print(str(e))

    # Checks if changes have been made based on a code passed
    def updateChanges(self,code):
        if code == 0 and not self.changed is None and not self.removed is None:
            self.whatsAdded.setText("")
            self.whatsRemoved.setText("")

            if len(self.changed) == 0:
                self.whatsAdded.append("Nothing Has Been Added!")

            else:
                for i in range(0, len(self.changed)):
                    self.whatsAdded.append("+ " + self.changed[i])

            if len(self.removed) == 0:
                self.whatsRemoved.append("Nothing Has Been Removed!")
            else:
                for i in range(0, len(self.removed)):
                    self.whatsRemoved.append("- " + self.removed[i])
        elif code == 1:
            secondaryWindows.messageWindow("Error","Error comparing files",True)

    # Connect to the database
    def startDatabaseGrabber(self):
        # connect to database to pull down primary files
        thread = DatabaseGrabber(self.window)
        thread.setup(self, getDatabaseAddress(), getDatabaseUsername(), self.databasePassword, getDatabase())
        thread.trigger.connect(self.fillComboBox)
        thread.start()

    # Get file timestamps
    def startHistoryGrabber(self,selectedFile):
        thread = SelectedFileGrabber(self.window)
        thread.setup(self, getDatabaseAddress(), getDatabaseUsername(), self.databasePassword,getDatabase(),selectedFile)
        thread.trigger.connect(self.updateDots)
        thread.start()

    # Refreshes the maintenance page
    def refreshPage(self):
        self.canUseCombobox = False
        if self.blocked:
            secondaryWindows.messageWindow("Process is currently running", "Cannot refresh", False)
        else:
            # clear fields
            self.commitDescription.setText("")
            self.commitTitle.setText("")
            self.whatsRemoved.setText("")
            self.whatsAdded.setText("")
            self.selectedConfig.clear()
            self.openFileButton.setText("Select File")
            self.fileToPush = None
            self.dots.clear()

            layout = self.commitDotLayout.layout()
            self.clearLayout(layout)
            dot = QRadioButton()
            dot.setText("Commits Appear Here")
            dot.setStyleSheet("border: 1px solid rgb(96,125,139);")
            layout.insertWidget(0, dot)
            self.dots.append(dot)

            self.startDatabaseGrabber()

            self.getFileHistory()

    # Gets the file from the FTP Server
    def startGrabber(self):
        self.selectedConfig.clear()
        # this is the users first step so get the password if we don't already have it for later
        # start the database grabber
        self.startDatabaseGrabber()

    def fillComboBox(self, code):
        self.canUseCombobox = False
        if code == 0 and not self.confFiles == None:  # only deal with conf code from deployment class
            nameList = list(self.confFiles.keys())
            nameList.sort()
            for index in range(len(nameList)):
                self.selectedConfig.addItem(nameList[index])
        elif code == 1:  # only deal with conf code from deployment class
            self.selectedConfig.addItem("None Present")
        elif code == -1:
            secondaryWindows.messageWindow("Error",
                                           "An error occured pulling down info from the database, check your details and try again",
                                           True)
        elif self.confFiles == None:
            secondaryWindows.messageWindow("Error",
                                           "An error occured pulling down info from the database, check your details and try again",
                                           True)
        self.canUseCombobox = True

    #clears the widgets out of the current layout
    def clearLayout(self,layout):
        while layout.count():  # while there are still widgets
            child = layout.takeAt(0)  # take widget
            if child.widget() is not None:
                child.widget().deleteLater()  # if there was one to take then delete it

    def swapIndexes(self,list,a,b):
        tmp = list[b]
        list[b] = list[a]
        list[a] = tmp

    def dateLessThan(self,a,b):
        # is the current year less than the min?
        if int(a[2]) < int(b[2]):
            return True
        # is the current month less than the min?
        if int(a[1]) < int(b[1]):
            return True
        # is the current date less than the min?
        if int(a[1]) == int(b[1]):
            if int(a[0]) < int(b[0]):
                return True

        return False

    def timeLessThan(self,a,b):
        # is the current hour less than the min?
        if int(a[0]) < int(b[0]):
            return True
        # is the current minute less than the min?
        if int(a[0]) == int(b[0]):
            if int(a[1]) < int(b[1]):
                return True
            # is the current second less than the min?
            if int(a[1]) == int(b[1]):
                if float(a[2]) < float(b[2]):
                    return True
            return False

    # sort the timestamp list based on date/time
    def sortTimeStamps(self,timeStamps):
        if len(timeStamps) == 1:
            return timeStamps

        for j in range(0,len(timeStamps)):
            for i in range(1,len(timeStamps) - j):
                timeOne = timeStamps[i-1]
                spaceIndex = timeOne.index(" ")
                timeOneDate = timeOne[:spaceIndex]
                timeOneDateData = timeOne[:spaceIndex].split('-')

                timeTwo = timeStamps[i]
                spaceIndex = timeTwo.index(" ")
                timeTwoDate = timeTwo[:spaceIndex]
                timeTwoDateData = timeTwo[:spaceIndex].split('-')

                if self.dateLessThan(timeTwoDateData,timeOneDateData):
                    self.swapIndexes(timeStamps, i, i-1)
                #are they the same date? Compare the time
                elif timeTwoDate == timeOneDate:
                    currentTime = timeTwo[spaceIndex + 1:].split(':')
                    minTime = timeOne[spaceIndex + 1:].split(':')
                    if self.timeLessThan(currentTime, minTime):
                        self.swapIndexes(timeStamps, i, i-1)

        return timeStamps

    def updateDots(self,code):
        try:
            #first clear out layout
            #self.commitDotLayout
            self.dots.clear()
            layout = self.commitDotLayout.layout()
            self.clearLayout(layout)
            self.scrollArea.setWidgetResizable(True)
            if code == 0 and not self.currentFilesHistory == None:  # only deal with conf code from deployment class
                historyList = list(self.currentFilesHistory.keys())
                historyList = self.sortTimeStamps(historyList)
                for index in range (0,len(historyList)):
                    dot = QRadioButton()
                    dot.setText(historyList[index])
                    dot.setStyleSheet("border: 1px solid rgb(96,125,139);")
                    dot.clicked.connect(self.displayFile)
                    layout.insertWidget(0,dot)
                    self.dots.append(dot)

            elif code == 1:  # only deal with conf code from deployment class
                secondaryWindows.messageWindow("Error",
                                               "An error occured pulling down info from the database, check your details and try again",
                                               True)
            elif self.currentFilesHistory == None:
                secondaryWindows.messageWindow("Error",
                                               "An error occured pulling down info from the database, check your details and try again",
                                               True)

        except Exception as e:
            print(str(e))

    def getContentsOfFile(self):
        returnString = StringIO()  # IO object to be written to like a file
        ftpAddress = getFtpAddress()
        selectedFile = self.fileToPull
        ftp = FTP(ftpAddress)
        ftp.login(getFtpUsername(),self.ftpPassword)
        # write contents of file to object with new lines
        ftp.retrlines('RETR ' + selectedFile, lambda line: returnString.write(line + '\n'))
        self.pulledFilesContents = returnString.getvalue()

    #  opens the explorer to get the file specified
    def openExplorer(self):
        try:
            #path returned as tuple though we just want the actual path
            name,_ = QFileDialog.getOpenFileName(self.window, 'Open File', options=QFileDialog.DontUseNativeDialog)
            if len(name) < 1:
                return
            start = self.findLast(name, "/") + 1
            filename = name[start:]
            extension = filename[len(filename) - 5:]
            if not ".conf" == extension:
                secondaryWindows.messageWindow("Not a configuration file", "Please select a configuration file to push",False)
                return
            self.openFileButton.setText(name[start:])
            self.fileToPush = name
        except Exception:
            secondaryWindows.messageWindow("Error",
                                           "Error parsing file, please ensure "
                                           "it's a .conf file with a suitable filename",
                                           True)

    def startPush(self):
        if not self.blocked:
            if self.fileToPush is None:
                secondaryWindows.messageWindow("No File Selected", "Please select a file to push", False)
                return
            elif len(self.commitTitle.text()) < 1:
                secondaryWindows.messageWindow("No Commit Title", "Please enter a title for your commit", False)
                return
            elif len(self.commitDescription.toPlainText()) < 1:
                secondaryWindows.messageWindow("No Commit description", "Please enter a description for your commit", False)
                return

            selectedTimeline = self.selectedConfig.currentText()

            #see if they want to commit to that files timeline
            reply = QMessageBox.question(self.window, 'Confirmation', "Are you sure you want to push to " + selectedTimeline + "'s timeline?", QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.blocked = True
                thread = RepoInterface(self.window)
                thread.setup(self)
                thread.trigger.connect(self.finishedPushingToRepo)
                thread.start()
            else:
                return
        else:
            secondaryWindows.messageWindow("Process is currently running", "There is still a file being pushed",False)

    def finishedPushingToRepo(self, code):
        self.blocked = False
        if code == 0:
            self.refreshPage()
            secondaryWindows.messageWindow("Success!", "Updated the repository successfully", False)
        else:
            secondaryWindows.messageWindow("Error", "Error pushing the files to the repository", False)

class FileComparer(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(FileComparer, self).__init__(parent)

    def setup(self, callingWindow):
        self.callingWindow = callingWindow

    def run(self):
        try:
            self.callingWindow.compareFiles()
            self.trigger.emit(0)
        except:
            self.trigger.emit(1)

# File grabber class to get files off UI thread
class DatabaseGrabber(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(DatabaseGrabber, self).__init__(parent)

    def setup(self, callingWindow,dbAddr,dbUser,dbPswd,db):
        self.callingWindow = callingWindow
        self.dbAddr = dbAddr
        self.dbUser = dbUser
        self.dbPswd = dbPswd
        self.db = db
    def run(self):
        try:
            listing = getDatabaseFileListing(self.dbAddr,self.dbUser,self.dbPswd,self.db)
            if not listing is None:
                self.callingWindow.confFiles = listing
                self.trigger.emit(0)
            else:
                self.trigger.emit(1)
        except:
            self.trigger.emit(-1)

'''
using the selected file from the combobox you serach the database for the other nonprimary entries
so you have a timeline to display on the commits dots
'''
class SelectedFileGrabber(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(SelectedFileGrabber, self).__init__(parent)

    def setup(self, callingWindow,dbAddr,dbUser,dbPswd,db, selectedFile):
        self.callingWindow = callingWindow
        self.dbAddr = dbAddr
        self.dbUser = dbUser
        self.dbPswd = dbPswd
        self.selectedFile = selectedFile
        self.db = db
    def run(self):
        try:
            self.callingWindow.currentFilesHistory = getCurrentFilesHistory(self.dbAddr,self.dbUser,self.dbPswd,self.db, self.selectedFile)
            self.trigger.emit(0)
        except:
            self.trigger.emit(1)

def getCurrentFilesHistory(dbAddr,dbUsr,dbPswd,database,selectedFile):
    connection = None
    cursor = None
    try:
        table = getDatabaseTable()
        connection = pymysql.connect(host=dbAddr, port=3306, user=dbUsr, passwd=dbPswd, db=database)
        cursor = connection.cursor()
        expression = "SELECT timestamp,path FROM " + table + " where name = \""+selectedFile+ "\";"
        cursor.execute(expression)
        response = cursor.fetchall()
        if response:  # if we've returned something
            cursor.close()
            connection.close()  # close connection first
            listingsLength = len(response)
            databaseListing = dict()  # start an empty dict for names to paths
            # list out data passed in as argument (pulled from database)
            for listings in range(0, listingsLength):
                listingEntry = response[listings]
                timestamp = str(listingEntry[0])
                path = str(listingEntry[1])
                databaseListing[timestamp] = path
            return databaseListing
        else:
            cursor.close()
            connection.close()
            return None
    except pymysql.OperationalError as e:
        print(str(e))
        return None
    except Exception as e:  # any issue assume no clear connection to database
        print(str(e))
        if not cursor is None:
            cursor.close()
        if not connection is None:
            connection.close()
        return None

def getDatabaseFileListing(dbAddr,dbUsr,dbPswd,database):
    connection = None
    cursor = None
    try:
        table = getDatabaseTable()
        connection = pymysql.connect(host=dbAddr, port=3306, user=dbUsr, passwd=dbPswd, db=database)
        cursor = connection.cursor()
        cursor.execute("SELECT name,path,isPrimary FROM " + table + " where isPrimary = 1;")  # return a limit of 100 listings
        response = cursor.fetchall()
        if response:  # if we've returned something
            cursor.close()
            connection.close()  # close connection first
            listingsLength = len(response)
            databaseListing = dict()  # start an empty dict for names to paths
            # list out data passed in as argument (pulled from database)
            for listings in range(0, listingsLength):
                listingEntry = response[listings]
                name = str(listingEntry[0])
                path = str(listingEntry[1])
                databaseListing[name] = path
            return databaseListing
        else:
            cursor.close()
            connection.close()
            return None
    except pymysql.OperationalError:
        return None
    except:  # any issue assume no clear connection to database
        if not cursor is None:
            cursor.close()
        if not connection is None:
            connection.close()
        return None

class RepoInterface(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent=None):
        super(RepoInterface, self).__init__(parent)

    def setup(self, callingWindow):
        self.callingWindow = callingWindow

    def run(self):
            if addToRepo(self.callingWindow):
                self.trigger.emit(0)
            else:
                self.trigger.emit(1)

#  pushes file to repository
def addToRepo(callingWindow):

    #Set variable values
    dbAddress = getDatabaseAddress()
    db = getDatabase()
    configTable = getDatabaseTable()
    dbUsername = getDatabaseUsername()
    dbPassword = callingWindow.databasePassword
    ftpUsername = getFtpUsername()
    ftpPassword = callingWindow.ftpPassword
    configName = callingWindow.selectedConfig.currentText()
    deviceSerial = ""
    configFile = callingWindow.fileToPush
    commitTitle = callingWindow.commitTitle.text()
    commitDesc= callingWindow.commitDescription.toPlainText()
    time = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S.%f')[:-4]
    newFileName = time.replace(":", "-")[:-3]
    newFileName = newFileName.replace(" ", "_") + ".conf"

    # Get current Config details
    getSerial = ("select serial from " + configTable + " where name=\"" + configName + "\" and isPrimary=\"1\"")
    try:
        conn = None

        conn = pymysql.connect(host=dbAddress, port=3306, user=dbUsername, passwd=dbPassword, db=db)
        cursor = conn.cursor()
        cursor.execute(getSerial)
        deviceSerial = cursor.fetchone()[0]
        conn.close()
    except Exception as e:
        print("Serial couldn't be recovered." + str(e))
        if not conn is None:
            conn.close()

    #Upload file to the FTP Server
    ftpAddress = getFtpAddress()
    path = getConfPath()
    fileContents = ""
    try:
        conn=None
        ftp=None

        #chck if conf file
        if not "conf" in configFile:
            messageWindow("Error!","Make sure that you are uploading a .conf file,",True)
            return False
        else:
            # Log into FTP
            ftp = FTP(ftpAddress)
            ftp.login(ftpUsername,ftpPassword)
            ftp.cwd(path)
            #Upload the file
            file = open(configFile, "rb")
            ftp.storlines('STOR ' + newFileName, file)
            ftp.close()
            file.close()

            # Get current config info
            updateCurentRecord = (
            "update " + configTable + " set " + "isPrimary=\"0\"" + " where name=\"" + configName + "\" and isPrimary=\"1\"")

            # Send new config details
            newFileNamePath = path+newFileName
            addNewRecord = (
            "insert into " + configTable + "(name,serial,user,timestamp,path,title,description,isprimary)" +
            " values (\"" + configName + "\", \"" + deviceSerial + "\",\"" + dbUsername + "\",\"" + time + "\",\"" + newFileNamePath + "\", \"" + commitTitle + "\", \"" + commitDesc + "\", 1)")

            # Push the data to the database

            conn = pymysql.connect(host=dbAddress, port=3306, user=dbUsername, passwd=dbPassword, db=db)
            cursor = conn.cursor()
            cursor.execute(updateCurentRecord)
            cursor.execute(addNewRecord)
            conn.commit()
            conn.close()
            return True

    except Exception as e:
        print(str(e))
        if not conn is None:
            conn.close()
        if not ftp is None:
            ftp.close()
        return False