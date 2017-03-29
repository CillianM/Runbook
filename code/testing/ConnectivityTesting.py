import unittest

from Connectivity import *

patch_crypto_be_discovery()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("redbrick.dcu.ie", 22, "user", "pass")
term = ssh.invoke_shell()

'''
.......
----------------------------------------------------------------------
Ran 9 tests in 24.072s

OK

'''

class LoginManagerTest(unittest.TestCase):
    global ssh,term

    def test_ping(self):
        self.assertTrue(pingAddress("192.168.0.1"))
        self.assertFalse(pingAddress("192.168.10.1"))

    def test_isJunosDevice(self):
        self.assertFalse(isJunosDevice("192.168.0.10"))

    def test_patch(self):
        patch_crypto_be_discovery() # ensure it works without error

    def test_sendCommand(self):
        send_command(term,"ls")

    def test_waitForLogin(self):
        waitForLogin(term)

    def test_waitForTerm(self):
        waitForTerm(term,1,"")

    def test_checkDbConnection(self):
        self.assertTrue(checkDatabaseConnection("password"))
        self.assertFalse(checkDatabaseConnection("pass"))
        self.assertFalse(checkDatabaseConnection(2))

    def test_checkFtpConnection(self):
        self.assertTrue(checkFTPConnection("password"))
        self.assertFalse(checkFTPConnection("pass"))
        self.assertFalse(checkFTPConnection(2))

    def test_consoleConnection(self):
        self.assertTrue(checkConsoleConnection("redbrick.dcu.ie","user", "pass"))
        self.assertFalse(checkConsoleConnection("redbrick.dcu.ie","user", "55"))
        self.assertFalse(checkConsoleConnection("redbrick.dcu.ie", "user", 22))





if __name__ == '__main__':
    unittest.main()