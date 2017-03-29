from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from customStyling import getVerticalScrollStyle,getHorizontalScrollStyle, ImageLable, IconLineEdit
from datetime import datetime

# Gloabal var - used to export database to a csv file
csvData = None

# Default alert/message window
def messageWindow(textHeader, textToDisplay,isError):
    msg = QMessageBox()
    #Is it just an information popup or an error message (just affects the icon displayed)
    if isError:
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
    else:
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Notification")
    msg.setText(textHeader)
    msg.setDetailedText(textToDisplay)
    msg.exec_()

# Window to display database information
def displayDatabaseWindow(listing):
    dialog = QDialog()
    dialog.setWindowIcon(QIcon('images/icon.ico'))
    dialog.setWindowTitle("Database Results")
    dialog.setStyleSheet("background-color: rgb(69,90,100);")
    dialog.setMinimumWidth(900)
    mainLayout = QHBoxLayout(dialog)

    container = QVBoxLayout()
    gridLayout = QGridLayout()

    heading = QLabel()
    heading.setText("Name")
    heading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
    heading.setWhatsThis("This is the filename given to what's pushed to the database")
    gridLayout.addWidget(heading, 0, 0)

    heading = QLabel()
    heading.setText("Serial Number")
    heading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
    heading.setWhatsThis("This is the serial number pulled from the device")
    gridLayout.addWidget(heading, 0, 1)

    heading = QLabel()
    heading.setText("User")
    heading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
    heading.setWhatsThis("This is the user who made this push to the database")
    gridLayout.addWidget(heading, 0, 2)

    heading = QLabel()
    heading.setText("Timestamp")
    heading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
    heading.setWhatsThis("This is the time that it took place")
    gridLayout.addWidget(heading, 0, 3)

    heading = QLabel()
    heading.setText("Config Path")
    heading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
    heading.setWhatsThis("This is the path to the config file used")
    gridLayout.addWidget(heading, 0, 4)

    heading = QLabel()
    heading.setText("Entry Title")
    heading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
    heading.setWhatsThis("This is the heading given to this database entry")
    gridLayout.addWidget(heading, 0, 5)

    heading = QLabel()
    heading.setText("Description")
    heading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
    heading.setWhatsThis("This is the description given to this database entry")
    gridLayout.addWidget(heading, 0, 6)

    heading = QLabel()
    heading.setText("Is Current Configuration")
    heading.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
    heading.setWhatsThis("This is to distinguish which configurations are currently in use")
    gridLayout.addWidget(heading, 0, 7)

    listingsLength = len(listing)
    entryLength = len(listing[0])
    row = 1
    col = 0

    # Export to CSV window formatting
    global csvData
    csvData = ["Name,Serial Number,User,Timestamp,Config Path,Entry Title,Description,Is Current Configuration"]
    # list out data passed in as argument (pulled from database)
    for listings in range(0,listingsLength):
        listingEntry = listing[listings]
        tmp = ""
        for entry in range(1,entryLength):
            text = QLabel()
            text.setText(str(listingEntry[entry]))
            text.setStyleSheet("border: 1px solid black; background-color: rgb(255,255,255); font-size:16px;")
            gridLayout.addWidget(text, row, col)
            tmp += str(listingEntry[entry]) + ","
            col += 1
        col = 0
        row += 1
        csvData.append(tmp[:len(tmp)-1])

    container.addLayout(gridLayout)
    exportButton = QPushButton("Export to CSV")
    exportButton.setStyleSheet("background-color: rgb(0,188,212); font-size:16px;")
    exportButton.clicked.connect(exportToCSV)
    container.addWidget(exportButton)

    viewport = QWidget()
    viewport.setLayout(container)

    scrollArea = QScrollArea()
    scrollArea.setStyleSheet(getHorizontalScrollStyle() + getVerticalScrollStyle())
    scrollArea.setWidget(viewport)
    mainLayout.addWidget(scrollArea)

    dialog.setAttribute(Qt.WA_DeleteOnClose)
    dialog.exec_()

#Export the database contents to a Excel readable CSV file
def exportToCSV():
    global csvData
    exportFileName = str(datetime.utcnow().strftime('%d-%m-%Y_%H-%M')) + ".csv"
    if not csvData is None:
        file = None
        try:
            file = open(exportFileName,"w")
            for i in range(0,len(csvData)):
                file.write(csvData[i]+"\n")
            file.close()
            messageWindow("Success!", "CSV file exported.", False)
        except Exception as e:
            if not file is None: file.close()
            messageWindow("Error!","CSV file generation failed.",True)
        csvData = None
    else:
        messageWindow("Error!", "CSV file generation failed.", True)