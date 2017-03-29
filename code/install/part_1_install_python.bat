::Python 3.6 install
bitsadmin /transfer Python /priority high https://www.python.org/ftp/python/3.6.0/python-3.6.0.exe c:\python-3.6.0.exe
cd C:\
python-3.6.0.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 PrependPath=1 AssociateFiles=1 Include_test=0
exit