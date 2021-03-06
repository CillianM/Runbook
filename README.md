# Network Deployment Automation Maintenance Tool

### Deployment Module
<img src="http://i.imgur.com/DtyRRv6.png=100x20" width="48">
This module sets up Juniper devices and updates JUNOS

### Maintenance Module 
<img src="http://i.imgur.com/BBpabPb.png" width="48">
This module connects to a database and an FTP server to provide version control of your config files used with devices 

### Troubleshooting Module 
<img src="http://i.imgur.com/9uXJKq3.png" width="48">
This module lets you scan your network and log in to devices you have access to for system information (CPU/RAM usage, etc.)

### Prerequisites: 
+ Your own FTP server with users, Logged in user must have read write access
+ Your own database with the schema described in the sql file in /code/runbook.sql
+ To make use of the deployment module a console server is required

### Libraries Required: 
[xmltodict](https://pypi.python.org/pypi/xmltodict)

[paramiko](http://www.paramiko.org/)

[PYQT5](https://www.riverbankcomputing.com/software/pyqt/download5) 

[NetworkX](https://networkx.github.io/)

[Matplotlib](http://matplotlib.org/)

[Pymysql](https://github.com/PyMySQL/PyMySQL)

#### Troubleshooting
+ Paramiko has problems installing on some distros of linux so look to their support page if you're having trouble building it
+ If you have any issues with the application itself contact [Cillian](https://gitlab.computing.dcu.ie/mcneilc2) or [Filip](https://gitlab.computing.dcu.ie/nikolif2) along with what you were doing and what went wrong at the time