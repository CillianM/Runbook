import subprocess
import ipaddress
import socket
import platform
import sys
import uuid

#Parse the arp table for the appropriate mac address
import networkx as nx
import matplotlib.pyplot as plt

def find(s, ch):
    list =  [i for i, ltr in enumerate(s) if ltr == ch]
    return list[-1]


def getMacAddr(currentOS, arpTable, currentIP):
    if("Windows" in currentOS):
        index = arpTable.index(currentIP) + len(currentIP) + 10
        return arpTable[index:index + 17]
    elif("Darwin" in currentOS or "Linux" in currentOS):
        index = arpTable.index(currentIP) + len(currentIP) + 5
        return arpTable[index:index + 17]
'''
if we can't just pick up IP address we can force a connection
and see what made address made that connection
'''
def getIpAddress():
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.connect(("136.206.1.4",80))
    return mySocket.getsockname()[0]

def scanNetwork(self):
    currentOS = platform.system()

    #Convert mac address from decimal to hex and add colons for readibility
    myMacAddress = hex(uuid.getnode())[2:]
    myMacAddress = ":".join(myMacAddress[i:i+2] for i in range(0,len(myMacAddress),2))

    myIpAddress = socket.gethostbyname(socket.gethostname())
    ipAddress = myIpAddress + "/24"

    #Issue when using WLan cards, get Loopback instead of actual IP address
    if("127.0" in ipAddress):
        ipAddress = getIpAddress() + "/24"

    ipNetwork = ipaddress.ip_network(ipAddress, strict=False)
    allHosts = list(ipNetwork)

    liveIPs = [myIpAddress]

    for i in range(len(allHosts)):
        currentIP = str(allHosts[i])
        if(currentIP != myIpAddress):
            #Windows
            if("Windows" in currentOS):
                output = subprocess.Popen(['ping', '-n', '1', '-w', '500', currentIP], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

                if "Reply from" in output:
                    liveIPs.append(currentIP)

            #Linux
            if ("Linux" in currentOS):
                output = subprocess.Popen(['ping', '-c', '1', '-w', '250', str(allHosts[i])], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

                if " 0% packet loss" in output:
                    liveIPs.append(currentIP)

            #Mac OS
            if ("Darwin" in currentOS):
                output = subprocess.Popen(['ping', '-c', '1', '-W', '500', str(allHosts[i])], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

                if " 0.0% packet loss" in output:
                    liveIPs.append(currentIP)

        currentPercentage = (i/len(allHosts)) * 100
        self.trigger.emit(currentPercentage)

    #Just make sure 100 is printed at the end due to decimals and rounding
    self.trigger.emit(100)
    '''
    get arp table once all ips have been ping-ed
    could run into problems getting arp on linux due to sudo
    '''
    arpTable = subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")

    G=nx.Graph()
    G.add_node(str(myIpAddress))
    #print out the live IPs along with their mac addresses found from the arp table
    for i in range(len(liveIPs)):
        if(liveIPs[i] != myIpAddress):
            macAddr = getMacAddr(currentOS, arpTable, liveIPs[i])
            oldIpString = str(liveIPs[i])
            newIPIndex = find(str(liveIPs[i]),'.')
            newIpString = oldIpString[newIPIndex:len(str(liveIPs[i])) + 1]
            #print(str(liveIPs[i]) + " (" + macAddr + ") is online")
            G.add_node(newIpString)
            edge = (newIpString, str(myIpAddress))
            G.add_edge(*edge)
        else:
            macAddr = myMacAddress


    nx.draw_networkx(G)
    plt.axis('off')
    plt.autoscale()
    plt.savefig("network_path.png", bbox_inches='tight') # save as png
    self.trigger.emit(101)


