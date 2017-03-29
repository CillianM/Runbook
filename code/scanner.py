import ipaddress
import platform
import socket
import subprocess
import threading
import urllib.request
import uuid

import networkx as nx
from PyQt5.QtCore import pyqtSignal
from Connectivity import pingAddress

# Used to generate an image of a Local Area Network
class Scanner():
    def __init__(self):
        super(Scanner, self).__init__()
        self.missingIpNumbers = None
        self.graphLocation = None
        self.macAddrDict = dict()
        self.vendorDict = dict()

    # get the ip numbers removed when they were added to graph (for readibility)
    def getMissingIpNumbers(self):
        return self.missingIpNumbers

    # to be called from outside to get vendor
    def returnVendor(self,macAddr):
        if macAddr in self.vendorDict:
            return self.vendorDict[macAddr]
        else:
            return "N/A"

    # to be called from outside to get mac address
    def returnMacAddr(self,ipAddr):
        if ipAddr in self.macAddrDict:
            return self.macAddrDict[ipAddr]
        else:
            return "N/A"

    # return the generated graph
    def getGraph(self):
        return self.graphLocation

    # checks if we're connected to the internet by pinging google
    def isConnected(self):
        try:
            urllib.request.urlopen("https://www.google.ie")
            return True
        except:
            return False

    def findLast(self,s, ch):
        #builds a list of all the occurences of a character
        list =  [index for index, currentChar in enumerate(s) if currentChar == ch]
        #returns the last index
        return list[-1]

    # depending on the OS, make the appropriate commands to get the submask for the network
    def getSubnetMask(self):
        try:
            os = platform.system()
            myIp = self.getMyIpAddr()
            notation = 0
            if "Windows" in os:
                ipconfig = subprocess.Popen(['ipconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")
                subnetMask = [line for line in ipconfig.split('\n') if "Subnet Mask" in line][0]
                start = subnetMask.index(':') + 1  # from start of subnet mask in ifconfig get the start of address
                end = self.findLast(subnetMask, '.') + 4  # get last few digits
                subnetMask = subnetMask[start:end].strip()
            elif "Linux" in os:
                ipconfig = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")
                subnetMask = [line for line in ipconfig.split('\n') if myIp in line][0]
                start = subnetMask.index("Mask") + 5  # locate where mask starts
                end = self.findLast(subnetMask, '.') + 4  # get last few digits
                subnetMask = subnetMask[start:end].strip()

            elif "Darwin" in os: #mac readout is a bit different as it's in hex
                ipconfig = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")
                subnetMask = [line for line in ipconfig.split('\n') if myIp in line][0]
                start = subnetMask.index("netmask") + 10  # locate where mask starts
                end = self.findLast(subnetMask, 'b')  # get last few digits
                subnetMask = subnetMask[start:end].strip()
                tmp = int(subnetMask,16)
                tmp = bin(tmp)[2:]
                for i in range(0,len(tmp)):
                    if not tmp[i] is "0":
                        notation += 1
                return "/" + str(notation)

            subnetMaskComponents = subnetMask.split('.')
            for i in range(0,len(subnetMaskComponents)):
                tmp = int(subnetMaskComponents[i])
                tmp = bin(tmp)[2:]
                if not tmp is "0":
                    notation += len(tmp)

            return "/" + str(notation)
        except:
            return "/24" #return a default value

    # consult arp table for mac addr
    def getMacAddr(self,currentIP):
        arpTable = self.getArpTable()
        currentOS = platform.system()
        '''
        ensure we're getting the entry for this ip rather than finding it within another
        eg. 192.168.1 is in 192.169.10
        so by having a ending character we avoid this
        '''
        macSpace = ':' #  linux and mac space mac address with :
        if "Windows" in currentOS:
            macSpace = '-' #  mac addresses spaced with - in windows
            currentIP = currentIP + " " #space after end of ip in arp table
        else:
            currentIP = currentIP + ")" #bracket in linux and mac
        try:
            arpEntry =  [line for line in arpTable.split('\n') if currentIP in line][-1] #get last index of lines found

            start = arpEntry.index(macSpace) - 2 # get first 2 characters of mac address
            end = self.findLast(arpEntry,macSpace) + 3 #get last 2 characters of mac address
            '''
            ff-ff-ff-ff-ff-ff
              ^           ^
            ff-ff-ff-ff-ff-ff => 2 and plus 3
            ^                ^
            '''
            return arpEntry[start:end].strip()
        except:
            return "Not in arp table"

    # gets my mac address through python command
    def getMyMacAddr(self):
        # Convert mac address from decimal to hex and add colons for readibility
        myMacAddress = hex(uuid.getnode())[2:]
        return ":".join(myMacAddress[i:i + 2] for i in range(0, len(myMacAddress), 2))

    '''
    Contacting https://macvendors.com/ through their API to get vendor for specified mac address
    returns the vendor or "vendor not found" otherwise
    '''
    def getMacVendor(self,macAddr):
        if not len(macAddr) == 17:
            return "N/A"
        #if we have internet connection get it through the API
        if self.isConnected():
            try:
                response = urllib.request.urlopen('http://api.macvendors.com/' + macAddr)
                vendor = str(response.read())
                return vendor[2:len(vendor) - 1] #just cut out quotes from returned string for neatness
            except:
                return self.checkMacFile(macAddr) #check locally is there was an error
        #otherwise we check our own local file
        else:
            return self.checkMacFile(macAddr)

    #checks for match in our local file
    def checkMacFile(self,macAddr):
        if not len(macAddr) == 17:
            return "N/A"
        macAddr = macAddr[:7]
        if "-" in macAddr:
            macAddr = self.removeMacSeperators(macAddr,"-")
        elif ":" in macAddr:
            macAddr = self.removeMacSeperators(macAddr,":")
        try:
            with open('mac_addresses.csv', 'r', encoding='utf-8') as f:
                for line in f:
                    comma = line.index(",")
                    prefix = line[:comma]
                    prefix = prefix.lower()
                    if macAddr in prefix:
                        return line[comma + 1:].strip('\n')
            return "N/A"
        except FileNotFoundError:
            return "No Local Record Found"

    def removeMacSeperators(self,macAddr,signToRemove):
        newMacAddr = ""
        for i in range(0,len(macAddr)):
            if macAddr[i] is not signToRemove:
                newMacAddr += macAddr[i]
        return newMacAddr

    # gets my ip through python command
    def getMyIpAddr(self):
        ipAddr =  socket.gethostbyname(socket.gethostname())
        # Issue when using WLan cards, get Loopback instead of actual IP address
        if ("127.0" in ipAddr):
            ipAddr = self.getIpAddressFix()
        return ipAddr

    '''
    if we can't just pick up IP address we can force a connection
    and see what made address made that connection
    '''
    def getIpAddressFix(self):
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mySocket.connect(("136.206.1.4",80))
        ip =  mySocket.getsockname()[0]
        mySocket.close()
        return ip

    # return the arp table
    def getArpTable(self):
        return subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")

    # start a scan of the network from a seperate thread
    def scanNetwork(self,callingThread):
        try:
            self.percentage = 0

            myIpAddress = self.getMyIpAddr()
            ipAddress = myIpAddress + self.getSubnetMask()

            ipNetwork = ipaddress.ip_network(ipAddress, strict=False)
            allHosts = list(ipNetwork)

            liveIPs = [myIpAddress]
            length = len(allHosts)

            chunkOne = []
            chunkTwo = []
            chunkThree = []
            chunkFour = []

            thread1 = SubScanner(1, myIpAddress, allHosts[0:int((length/4) +1)],chunkOne)
            thread1.start()

            thread2 = SubScanner(2, myIpAddress, allHosts[int((length/4) +1):int((length / 2) + 1)], chunkTwo)
            thread2.start()

            thread3 = SubScanner(3, myIpAddress, allHosts[int((length / 2) + 1):int((length / 4) + 1) * 3], chunkThree)
            thread3.start()

            thread4 = SubScanner(4, myIpAddress, allHosts[int((length / 4) + 1) * 3:length], chunkFour)
            thread4.start()

            #Small progress update to show them something is happening
            callingThread.trigger.emit(5)
            thread1.join()
            callingThread.trigger.emit(25)
            thread2.join()
            callingThread.trigger.emit(50)
            thread3.join()
            callingThread.trigger.emit(75)
            thread4.join()

            #bring all the found IPs back together
            liveIPs.extend(chunkOne)
            liveIPs.extend(chunkTwo)
            liveIPs.extend(chunkThree)
            liveIPs.extend(chunkFour)

            callingThread.trigger.emit(90)

            G=nx.Graph()
            G.add_node(str(myIpAddress))
            stringIndex = self.findLast(str(myIpAddress), '.')
            #so when we cut it down for the labels we still have what we cut out
            self.missingIpNumbers = myIpAddress[0:stringIndex]

            global macAddrDict,vendorDict
            myMac = self.getMyMacAddr()
            self.macAddrDict[myIpAddress] = self.getMyMacAddr()
            self.vendorDict[myMac] = self.getMacVendor(myMac)

            #Take all of our current IPs and construct the graph along with finding the mac and vendor
            for i in range(len(liveIPs)):
                if(liveIPs[i] != myIpAddress):
                    oldIpString = str(liveIPs[i])
                    newIPIndex = self.findLast(str(liveIPs[i]), '.')
                    newIpString = oldIpString[newIPIndex:len(str(liveIPs[i])) + 1]
                    G.add_node(newIpString)
                    edge = (newIpString, str(myIpAddress))
                    G.add_edge(*edge)
                    currentMac = self.getMacAddr(liveIPs[i])
                    self.macAddrDict[liveIPs[i]] = currentMac
                    self.vendorDict[currentMac] = self.getMacVendor(currentMac)

            callingThread.trigger.emit(100)

            self.graphLocation = G
            callingThread.trigger.emit(101)
        except Exception as e:
            print(str(e))
            callingThread.trigger.emit(-1)

# Used for pinging LAN devices
class SubScanner(threading.Thread):
    trigger = pyqtSignal(int)

    def __init__(self, thread_no, myIpAddress, listToScan,listToReturn):
        threading.Thread.__init__(self)
        self.thread_no = thread_no
        self.currentOS = platform.system()
        self.myIpAddress = myIpAddress
        self.listToScan = listToScan
        self.listToReturn = listToReturn

    def run(self):
        for i in range(len(self.listToScan)):
            currentIP = str(self.listToScan[i])
            if (currentIP != self.myIpAddress):
                if pingAddress(currentIP):
                    self.listToReturn.append(currentIP)
