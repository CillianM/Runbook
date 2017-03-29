# **Testing Reports**

All documentation below is in reference to the reports found [here](https://www.redbrick.dcu.ie/~minisham/YR3_PROJ/) along with the files found in [/code/testing](https://gitlab.computing.dcu.ie/mcneilc2/2017-CA326-Cillian-Network_Deployment_Automation_Maintenance_Tool/tree/master/code/testing)

# **Testing Overview**

Below we will go over how we came about constructing these reports and what went into giving us the coverage described. We took a whitebox approach to all of our testing so that we could eliminate any errors as we went along. As this was to be presented in the coming weeks we wanted any glaring issues to be ironed out before then. The testing mainly revolved around code coverage using unit testing, boundary value testing & path testing to ensure the correct operation was carried out for each respective method, value and boolean.

##   
**Unit Testing**

The application was designed to be flexible and expandable. This means that both the classes and methods within the programme are seperated out into what function they offer. This allows for the construction of additional modules later on if desired.  
When it came to testing the programme the logical option was to seperate out these files,classes and methods into units and test each one for their functionality. Sometimes this couldn't be accomplished due to the nature of PyQt. To combat this we would construct mini windows in which seperate parts of the programme could be displayed. We would then run our tests on those windows. Once those tests were run values were stored within the respective class and further tests could be used to validate the data going in or out. An example of this is the LoginManager, passwords and intents are passed into the programme through the GUI and our unit tests assert whether these are set to the appropriate values. By doing unit tests in this fashion we can ensure code coverage using different or incorrect values and see if any errors are raised along the way.  

##   
**Boundary Value Testing**

An extension of the unit testing performed was boundary value testing. A lot of the application's inputs and outputs are generated within the programme itself so values are either going to come out formatted correctly or throw an error. In some cases we have user's input for passwords, desired configs or submission descriptors. The bulk of these have no bearing on the performance of the application and in most cases will just result in the user not able to connect to a device due to an incorrect password/address. Despite all this we still needed to ensure that any value passed into these methods could be handled easily. By constructing different asserts within each test and through user testing we were able to take note of any faults that may arise as a result of user error and put guards in place to ensure they don't happen. The result of that can be seen within the reports above  

##   
**User Testing**

As this is a network engineer's tool we needed to ensure that they're able to understand and use this tool without any issues or errors arising. The user testing was carried out with a netwroking companu based in Dublin called [Agile networks](http://www.agilenetworks.ie/). We have the network engineers to test the application and bring up any issues they had with it. 

##   
**Deployment Module Testing**

The main functionality of this module depends on the device which is being configured, as well as the network on which the application is running.
Code coverage has been carried out on this module, as well as testing for incorrect user input, the other variables were handled by testing this module on different types of databases, console servers, FTP servers, as well as over ten different models of Juniper Networks devices. 

![user-testing](http://i.imgur.com/iB8IA0r.jpg)