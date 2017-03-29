import platform
import subprocess
import time
from ftplib import FTP

import paramiko
import pymysql

from settings import \
    getDatabaseAddress, \
    getDatabaseUsername, \
    getFtpAddress, \
    getFtpUsername

'''
General Methods Below to be used for connectivity across the application
'''

# Credit to exvito for patch
# link: https://github.com/pyca/cryptography/issues/2039
def patch_crypto_be_discovery():
    """
    Monkey patches cryptography's backend detection.
    Objective: support pyinstaller freezing.
    """
    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
        ]

def send_command(term, cmd):
    term.send(cmd + "\n")
    time.sleep(3)
    output = term.recv(188388) #bitsize to ensure correct buffer
    # Convert byte output to string
    output = output.decode("utf-8")
    return output

def waitForTerm(term, timeToWait, promptToWaitFor):
    timesChecked = 1
    ready = False
    while (not ready):
        time.sleep(timeToWait)
        answer = send_command(term, "")
        print(answer)
        if (promptToWaitFor in answer):
            ready = True
        timesChecked = timesChecked + 1

def waitForLogin(term,pswd):
    send_command(term, "root")
    time.sleep(2)
    send_command(term, pswd)
    time.sleep(2)
    send_command(term, "cli")

# check if the database specified is actually live and accessible through the parameters passed in
def checkDatabaseConnection(dbPswd):
    dbAddr = getDatabaseAddress()
    dbUsr = getDatabaseUsername()
    connection = None
    cursor = None
    try:
        connection = pymysql.connect(host=dbAddr, port=3306, user=dbUsr, passwd=dbPswd, db='runbook')
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        response = cursor.description
        if response:  # if we have anything in this request then we are connected and able to send and receive
            cursor.close()
            connection.close()
            return True
        else:
            cursor.close()
            connection.close()
            return False
    except pymysql.OperationalError:
        return False
    except:  # any issue assume no clear connection to database
        if not cursor is None:
            cursor.close()
        if not connection is None:
            connection.close()
        return False

# check if ftp server is live and accessible through the parameters specified
def checkFTPConnection(ftpPassword):
    try:
        ftpAddr = getFtpAddress()
        ftp = FTP(ftpAddr)
        username = getFtpUsername()
        ftp.login(username,ftpPassword)
        ftp.nlst()
        ftp.quit()
        return True
    except:
        return False

# check if console connection is live and accessible through the parameters specified
def checkConsoleConnection(conAddr,conUsr,conPswd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(conAddr, 22, conUsr, conPswd)
        ssh.close()
        return True
    except:
        return False

# check if it's a junos device
def isJunosDevice(addr):
    if pingAddress(addr):  # ping it to get mac
        from scanner import Scanner
        scanner = Scanner()
        macAddr = scanner.getMacAddr(addr)  # get mac address
        vendor = scanner.getMacVendor(macAddr)  # get the vendor
        if "Juniper" in vendor:  # if Juniper is the vendor then we can continue
            return True
        else:
            return False
    else:
        return False

# ping address specified
def pingAddress(addr):
    '''
    -n/-c ==> amount of packets to be sent
    -w/-W ==> timeout
    this can be adjusted to find optimal balance between quick and accurate checking
    '''
    currentOS = platform.system()
    # Windows
    if ("Windows" in currentOS):
        output = subprocess.Popen(['ping', '-n', '2', '-w', '250', addr],
                                  stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

        if "Reply from" in output:
            return True

    # Linux
    if ("Linux" in currentOS):
        output = subprocess.Popen(['ping', '-c', '2', '-w', '250', str(addr)],
                                  stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

        if " 0% packet loss" in output:
            return True

    # Mac OS
    if ("Darwin" in currentOS):
        output = subprocess.Popen(['ping', '-c', '2', '-W', '250', str(addr)],
                                  stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

        if " 0.0% packet loss" in output:
            return True

    return False