from tkinter import *
import threading
import tkinter.messagebox as tm
import paramiko
import time
import xmltodict
#viePaitah3
#10

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_1 = Label(self, text="Username")
        self.label_2 = Label(self, text="Address")
        self.label_3 = Label(self, text="Password")

        self.entry_1 = Entry(self)
        self.entry_2 = Entry(self)
        self.entry_3 = Entry(self, show="*")

        self.label_1.grid(row=0, sticky=E)
        self.label_2.grid(row=1, sticky=E)
        self.label_3.grid(row=2, sticky=E)
        self.entry_1.grid(row=0, column=1)
        self.entry_2.grid(row=1, column=1)
        self.entry_3.grid(row=2, column=1)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clickked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clickked(self):
        if len(self.entry_1.get()) < 1 or len(self.entry_2.get()) < 1:
            tm.showerror("Login Error","Enter a full name and address")
        else:
            patch_crypto_be_discovery()
            t = threading.Thread(target=_connect_session, args = (self.entry_1.get(),self.entry_2.get(),self.entry_3.get()))
            t.daemon = True
            t.start()
            tm.showinfo("Thread created", "You can add another device now")

def _connect_session(username,hostname,password):
    try:
        #replace port colon with underscore for filename
        filename = username.replace(":","_") + ".xml"
        print ("Filename will be " + filename)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, 22, username, password)
        term = ssh.invoke_shell()
        print(username + ": " +"Connected")
        #set cli screen-length 0
        checkRoot(term,5,"login",username)
        print(username + ": " +"Logged in")
        send_command(term, "set cli screen-length 0")
        xml = send_command(term, "show chassis hardware | display xml")
        xml = xml[37:(len(xml)) -10]
        text_file = open(filename, "w")
        text_file.write(xml)
        text_file.close()
        print(username + ": " +"Parsing xml for serial")
        parse_xml_serial(filename,username)

        send_command(term, "request system software add \"ftp://10.179.236.10/junos-srxsme-15.1X49-D50.3-domestic.tgz\" no-copy no-validate reboot")
        print(username + ": " +"Requested System software, waiting 2 minutes looped")
        check(term, 120,"login",username)
        print(username + ": " +"Logged in again")
        send_command(term, "request system snapshot media internal slice alternate")
        print(username + ": " +"Requested system snapshot, waiting 1 minute looped")
        check(term, 60,"root",username)
        print(username + ": " +"Request accepted, Partitioned snapshot")
        print(username + ": " +"Seraching Junos version")
        send_command(term, "set cli screen-length 0")
        output = send_command(term,"show system snapshot media internal | display xml")
        output = output[51:(len(output)) - 10]
        text_file = open(filename, "w")
        text_file.write(output)
        text_file.close()
        print(username + ": " +"Parsing Junos version")
        if(parse_xml_version(filename,term,username)):
            #_send_command(term, "delete /yes")
            #_send_command(term, "load set \"ftp://Administrator@10.179.236.10/config.conf\"")
            #_send_command(term,"set system login user Agile class super-user")
            #_send_command(term,"set system login user authentication plain-text-password")
            #_send_command(term, "password")
            #_send_command(term, "password")
            #_send_command(term, "commit-and quit")
            print(username + ": " +"Versions ok")
            send_command(term, "request system halt in 0")
            time.sleep(2)
            send_command(term, "yes")
        else:
            print(username + ": " +"Versions not configured properly")

        print(username + ": " + "Shutting down")
        send_command(term, "request system halt in 0")
        time.sleep(2)
        send_command(term,"yes")

        ssh.close()
        return
    except paramiko.ssh_exception.BadHostKeyException:
        tm.showerror("Host Key Error!","Server’s host key could not be verified")
    except paramiko.ssh_exception.AuthenticationException:
        tm.showerror("Authentication Error!", "Authentication failed, Check your details and try again")
    except paramiko.ssh_exception.SSHException:
        tm.showerror("Unknown Error!","Unknown error connecting or establishing an SSH session")




def send_command(term, cmd):
    term.send(cmd + "\n")
    time.sleep(3)
    output = term.recv(2024)
    # Convert byte output to string
    fOutput = output.decode("utf-8")
    # print(fOutput)
    return fOutput


def parse_xml_serial(xml,username):
    with open(xml) as fd:
        mydict = xmltodict.parse(fd.read())
    print(username + ": " +"Serial number is: {}".format(
        mydict['rpc-reply']['chassis-inventory']['chassis']['serial-number']
    ))


def parse_xml_version(xml, term,username):
    try:
        with open(xml) as fd:
            mydict = xmltodict.parse(fd.read())
        backupVersion= mydict['rpc-reply']['snapshot-information']['software-version'][0]['package']['package-version']
        primaryVersion = mydict['rpc-reply']['snapshot-information']['software-version'][1]['package']['package-version']
        print(username + ": " +"Primary Version: " + primaryVersion)
        print(username + ": " +"Backup Version " + backupVersion)
        if ("D50.3" in primaryVersion):
            print(username + ": " +"New Version updated")
            if (backupVersion == primaryVersion):
                print(username + ": " +"New Version updated")
                send_command(term, "configure")
                return True;
            else:
                return False;
        else:
            return False;
    except:
        print(username + ": " + "XML Parse Error, Skipping version check")
        return False;


def check( term, timeToWait, promptToWaitFor,username):
    timesChecked = 1
    ready = False
    while (not ready):
        print(username + ": " +"Checked "+ str(timesChecked) + " Times(s), Looping for another " + str(timeToWait) + " seconds waiting for " + promptToWaitFor)
        answer = send_command(term, "")
        #print(answer)
        if (promptToWaitFor in answer):
            if(promptToWaitFor == "login"):
                _login(term)
            ready = True
        timesChecked = timesChecked + 1
        time.sleep(timeToWait)

def checkRoot( term, timeToWait, promptToWaitFor,username):
    timesChecked = 1
    ready = False
    while (not ready):
        print(username + ": " + "Checked " + str(timesChecked) + " Times(s), Looping for another " + str(
            timeToWait) + " seconds waiting for " + promptToWaitFor)
        answer = send_command(term, "")
        # print(answer)
        if (promptToWaitFor in answer):
            _login(term)
            ready = True
        if (promptToWaitFor == "login" and "root" in answer):
            send_command(term, "exit")
            send_command(term, "exit")
            _login(term)
            ready = True
        timesChecked = timesChecked + 1
        time.sleep(timeToWait)


def _login( term):
    send_command(term, "root")
    send_command(term, "")
    send_command(term, "cli")


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

root = Tk()
lf = LoginFrame(root)
root.mainloop()