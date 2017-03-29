import unittest

from scanner import *

'''
This class is used to run unit tests on the scanner.py file and the
classes/methods contained in them
each test case has it's own scanner associated with it
assert equals will need to be changed based on the PC it's running on
'''

'''
RESULT:
............
----------------------------------------------------------------------
Ran 12 tests in 136.466s

OK

84% Coverage with 35 missing statements
30 of which are OS/Connectivity dependent
==> 98% Code coverage not counting these

'''

# single scanner for us to use and reference
scanner = Scanner()

class ScannerTest(unittest.TestCase):
    global scanner
    # test to see if ip matches what we have on cmd
    def test_getMyIp(self):
        self.assertEqual(scanner.getMyIpAddr(), "192.168.0.123")

    # test getting an ip through an internet connection
    def test_getIpAddressFix(self):
        self.assertEqual(scanner.getIpAddressFix(),"192.168.0.123")

    # test to see if mac matches what we have on cmd
    def test_getMyMac(self):
        self.assertEqual(scanner.getMyMacAddr(), "d0:50:99:5d:e3:94")

    # test that it checks our local file correctly
    def test_checkMacFile(self):
        myMac = scanner.getMyMacAddr()  # get my mac to check
        self.assertEqual(scanner.checkMacFile(myMac), "ASRock Incorporation") # test actual case
        self.assertEqual(scanner.checkMacFile(myMac[0:3]), "N/A") # test string too short
        self.assertEqual(scanner.checkMacFile(myMac + ":b9"), "N/A")  # test string too long
        self.assertNotEqual(scanner.checkMacFile(myMac), "No Local Record Found") # test to make sure file is there

    # test values for Mac addresses
    def test_getMacVendor(self):
        myMac = scanner.getMyMacAddr() #get my mac to check
        self.assertEqual(scanner.getMacVendor(myMac), "ASRock Incorporation")
        self.assertEqual(scanner.getMacVendor(myMac[0:3]), "N/A")  # test string too short
        self.assertEqual(scanner.getMacVendor(myMac + ":b9"), "N/A")  # test string too long

    # test that it correctly removes the sign specified
    def test_removeMacSeperators(self):
        myMac = scanner.getMyMacAddr()  # get my mac to check d0:50:99:5d:e3:94
        self.assertEqual(scanner.removeMacSeperators(myMac,":"), "d050995de394")
        self.assertEqual(scanner.removeMacSeperators(myMac[0:3],":"), "d0")  # test string too short
        self.assertEqual(scanner.removeMacSeperators(myMac + ":b9",":"), "d050995de394b9")  # test string too long
        self.assertEqual(scanner.removeMacSeperators(myMac + ":b9", "-"), "d0:50:99:5d:e3:94:b9")  # test different sign

    # test that subprocess is returned correctly
    def test_getArpTable(self):
        arpTable = subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")
        self.assertEqual(scanner.getArpTable(),arpTable)

    # start a scan of the network to be used to test later methods
    # NOTE: TO TEST THIS YOU NEED TO COMMENT OUT THE PYQT TRIGGERS
    def test_scanNetwork(self):
        scanner.scanNetwork("NOT A TRIGGER")
        # Now test that data was correctly compiled adn returned
        myMac = scanner.getMyMacAddr()
        myIp = scanner.getMyIpAddr()
        self.assertEqual(scanner.returnVendor(myMac), "ASRock Incorporation")
        self.assertEqual(scanner.returnVendor("ha"), "N/A")
        self.assertEqual(scanner.returnMacAddr(myIp), "d0:50:99:5d:e3:94")
        self.assertEqual(scanner.returnMacAddr("ha"), "N/A")
        self.assertNotEqual(scanner.getGraph(), None)
        self.assertEqual(scanner.getMissingIpNumbers(), "192.168.0")

    # test if we're connected to the internet
    def test_isConnected(self):
        self.assertTrue(scanner.isConnected())

    # test if we get the correct subnet mask
    def test_getSubnetMask(self):
        self.assertEqual(scanner.getSubnetMask(), "/24")

    # test if we can get the correct index of the last instance of the character
    def test_findLast(self):
        self.assertEqual(scanner.findLast("hello_hi","_"), 5)

    def test_getMacAddr(self):
        self.assertEqual(scanner.getMacAddr("192.168.0.10"),"54-60-09-03-e3-b0")
        self.assertEqual(scanner.getMacAddr("192.168.120.10"), "Not in arp table")
        self.assertEqual(scanner.getMacAddr("192.168.120"), "Not in arp table")

if __name__ == '__main__':
    unittest.main()