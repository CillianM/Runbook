import subprocess
import ipaddress
import socket
import platform
import threading
import uuid

#Parse the arp table for the appropriate mac address
import networkx as nx
from PyQt5.QtCore import pyqtSignal

graphLocation = None
liveIpAddresses = None
window = None

def find(s, ch):
    list =  [i for i, ltr in enumerate(s) if ltr == ch]
    return list[-1]


def getMacAddr(arpTable, currentIP):
    try:
        if("Windows" in platform.system()):
            index = arpTable.index(currentIP) + len(currentIP) + 10
            return arpTable[index:index + 17]
        elif("Darwin" in platform.system() or "Linux" in platform.system()):
            index = arpTable.index(currentIP) + len(currentIP) + 5
            return arpTable[index:index + 17]
    except:
        return "N/A"

def getMyMacAddr():
    myMacAddress = hex(uuid.getnode())[2:]
    return ":".join(myMacAddress[i:i + 2] for i in range(0, len(myMacAddress), 2))

def getMyIpAddr():
    return socket.gethostbyname(socket.gethostname())
'''
if we can't just pick up IP address we can force a connection
and see what made address made that connection
'''
def getIpAddress():
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.connect(("136.206.1.4",80))
    return mySocket.getsockname()[0]

def getArpTable():
    return subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")

def scanNetwork(self):
    global window
    window = self
    self.percentage = 0
    threads = []
    currentOS = platform.system()

    #Convert mac address from decimal to hex and add colons for readibility


    myIpAddress = getMyIpAddr()
    ipAddress = myIpAddress + "/24"

    #Issue when using WLan cards, get Loopback instead of actual IP address
    if("127.0" in ipAddress):
        ipAddress = getIpAddress() + "/24"

    ipNetwork = ipaddress.ip_network(ipAddress, strict=False)
    allHosts = list(ipNetwork)

    liveIPs = [myIpAddress]
    length = len(allHosts)

    chunkOne = []
    chunkTwo = []
    chunkThree = []
    chunkFour = []

    try:
        thread1 = SubScanner(1, myIpAddress, allHosts[0:int((length/4) +1)],chunkOne)
        thread1.start()

        thread2 = SubScanner(2, myIpAddress, allHosts[int((length/4) +1):int((length / 2) + 1)], chunkTwo)
        thread2.start()

        thread3 = SubScanner(3, myIpAddress, allHosts[int((length / 2) + 1):int((length / 4) + 1) * 3], chunkThree)
        thread3.start()

        thread4 = SubScanner(4, myIpAddress, allHosts[int((length / 4) + 1) * 3:length], chunkFour)
        thread4.start()

        #Small progress update to show them something is happening
        self.trigger.emit(5)
        thread1.join()
        self.trigger.emit(25)
        thread2.join()
        self.trigger.emit(50)
        thread3.join()
        self.trigger.emit(75)
        thread4.join()
    except Exception as e: print(str(e))

    #bring all the found IPs back together
    liveIPs.extend(chunkOne)
    liveIPs.extend(chunkTwo)
    liveIPs.extend(chunkThree)
    liveIPs.extend(chunkFour)


    #Just make sure 100 is printed at the end due to decimals and rounding
    self.trigger.emit(100)

    G=nx.Graph()
    G.add_node(str(myIpAddress))
    #print out the live IPs along with their mac addresses found from the arp table
    try:
        for i in range(len(liveIPs)):
            if(liveIPs[i] != myIpAddress):
                oldIpString = str(liveIPs[i])
                newIPIndex = find(str(liveIPs[i]),'.')
                newIpString = oldIpString[newIPIndex:len(str(liveIPs[i])) + 1]
                G.add_node(newIpString)
                edge = (newIpString, str(myIpAddress))
                G.add_edge(*edge)
    except Exception as e: print(str(e))


    #Allow access to final graph and returned IPs
    global graphLocation
    global liveIpAddresses
    graphLocation = G
    liveIpAddresses = liveIPs
    self.trigger.emit(101)

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
                # Windows
                if ("Windows" in self.currentOS):
                    output = \
                    subprocess.Popen(['ping', '-n', '1', '-w', '500', currentIP], stdout=subprocess.PIPE).communicate()[
                        0].decode('utf-8')

                    if "Reply from" in output:
                        self.listToReturn.append(currentIP)

                # Linux
                if ("Linux" in self.currentOS):
                    output = subprocess.Popen(['ping', '-c', '1', '-w', '250', str(self.listToScan[i])],
                                              stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

                    if " 0% packet loss" in output:
                        self.listToReturn.append(currentIP)

                # Mac OS
                if ("Darwin" in self.currentOS):
                    output = subprocess.Popen(['ping', '-c', '1', '-W', '500', str(self.listToScan[i])],
                                              stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

                    if " 0.0% packet loss" in output:
                        self.listToReturn.append(currentIP)

            currentPercentage = (i / len(self.listToScan)) * 25



