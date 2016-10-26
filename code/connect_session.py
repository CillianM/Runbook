from tkinter import *
import tkinter.messagebox as tm
import paramiko
import time
import xmltodict

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


    def _connect_session(self,username,hostname,password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, 22, username, password)
            term = ssh.invoke_shell()
            print("Connected")
            #set cli screen-length 0

            self._check(term,5,"login")
            self._login(term)
            print("Logged in")
            self._send_command(term, "set cli screen-length 0")

            xml = self._send_command(term, "show chassis hardware | display xml")
            xml = xml[37:(len(xml)) -10]
            text_file = open("Output.xml", "w")
            text_file.write(xml)
            text_file.close()
            print("Parsed xml")
            self._parse_xml_serial("Output.xml")

            self._send_command(term, "request system software add \"ftp://10.179.236.10/junos-srxsme-15.1X49-D60.7-domestic.tgz\" no-copy no-validate reboot")
            print("Requested System software, waiting 2 minutes looped")
            self._check(term, 120,"login")
            self._login(term)
            print("Logged in again")
            self._send_command(term, "request system snapshot media internal slice alternate")
            print("Requested system snapshot, waiting 1 minute looped")
            self._check(term, 60,"root")
            print("Request accepted, Partitioned snapshot")
            self._send_command(term, "set cli screen-length 0")
            print("Seraching Junos version")
            output = self._send_command(term,"show system snapshot media internal | display xml")
            output = output[51:(len(output)) - 10]
            text_file = open("Output.xml", "w")
            text_file.write(output)
            text_file.close()
            print("Parsing Junos version")
            if(self._parse_xml_version("Output.xml",term)):
                #self._send_command(term, "delete /yes")
                #self._send_command(term, "load set \"ftp://Administrator@10.179.236.10/config.conf\"")
                #self._send_command(term,"set system login user Agile class super-user")
                #self._send_command(term,"set system login user authentication plain-text-password")
                #self._send_command(term, "password")
                #self._send_command(term, "password")
                #self._send_command(term, "commit-and quit")
                print("Versions ok")
                self._send_command(term, "request system halt in 0 / yes")
            else:
                print("Versions not configured properly")

            ssh.close()
        except paramiko.ssh_exception.BadHostKeyException:
            tm.showerror("Host Key Error!","Server’s host key could not be verified")
        except paramiko.ssh_exception.AuthenticationException:
            tm.showerror("Authentication Error!", "Authentication failed, Check your details and try again")
        except paramiko.ssh_exception.SSHException:
            tm.showerror("Unknown Error!","Unknown error connecting or establishing an SSH session")

    def _login_btn_clickked(self):
        if len(self.entry_1.get()) < 1 or len(self.entry_2.get()) < 1:
            tm.showerror("Login Error","Enter a full name and address")
        else:
            self._connect_session(self.entry_1.get(),self.entry_2.get(),self.entry_3.get())

    def _send_command(self,term,cmd):
        term.send(cmd + "\n")
        time.sleep(3)
        output = term.recv(2024)
        #Convert byte output to string
        fOutput = output.decode("utf-8")
        #print(fOutput)
        return fOutput

    def _parse_xml_serial(self,xml):
        with open(xml) as fd:
            mydict = xmltodict.parse(fd.read())
        print("Serial number is: {}".format(
            mydict['rpc-reply']['chassis-inventory']['chassis']['serial-number']
        ))

    def _parse_xml_version(self,xml,term):
        with open(xml) as fd:
            mydict = xmltodict.parse(fd.read())
        oldVersion = mydict['rpc-reply']['snapshot-information']['software-version'][0]['package']['package-version']
        newVersion = mydict['rpc-reply']['snapshot-information']['software-version'][1]['package']['package-version']
        print("New Version: " + newVersion)
        print("Old Version " + oldVersion)
        if(newVersion == "15.1X49-D60.3-domestic"):
            print("New Version updated")
            self._send_command(term,"show system snapshot media internal")
            if(oldVersion == "15.1X49-D60.7-domestic"):
                print("New Version updated")
                self._send_command(term, "configure")
                return True;
            else:
                return False;
        else:
            return False;

    def _check(self,term,timeToWait,promptToWaitFor):
        ready = False
        while (not ready):
            time.sleep(timeToWait)
            print("Looping for another " + str(timeToWait) + " seconds waiting for " + promptToWaitFor)
            answer = self._send_command(term, "")
            print(answer)
            if (promptToWaitFor in answer):
                ready = True

    def _login(self,term):
        self._send_command(term, "root")
        self._send_command(term, "")
        self._send_command(term, "cli")

root = Tk()
lf = LoginFrame(root)
root.mainloop()