# __Johnny's Routing Report__

> This document uses Markdown.  Please view on Github (https://github.com/johnnywilkes/NPL_MAY_2019_ROUTES) or use the following for viewing: https://stackedit.io/app#

## ___Overall Program Idea___

> **Please note that this program uses the [Pandas](http://pandas.pydata.org) module.  If you don't have the Pandas module installed, it will prompt and error and quit.  Run `pip install pandas` to install.**

> **[TextFSM](https://github.com/google/textfsm/wiki/TextFSM) is also used in this program to parse the text file with the `show ip route` command and make it into a structured python data format.**

> **This program also assumes that you have selected the txt file to parse via command line argument or that you are going to parse a default file ('20190506_Route_Sample_1.txt') in the same directory as the script.**


The goal of this challenge was to parse a text file that contained "show ip route" output from an IOS device and to list the number of different routes (connected, EIGRP, local, OSPF and static).  My strategy is to always start simple as I knew this could be solved by regular expression or even the python string [count()](https://www.w3schools.com/python/ref_string_count.asp) method.  I decided to keep it simple and start with the count() method (see `my str_count` function) and then to build from there.  However, there are some disadvantages of this strategy:
 - Have to search for a set number of patterns (such as `S  ` and also `S* ` for static routes).
 - This is only a simple string search and doesn't help to put the whole output into structured python data format.
 
Thus, I decided to look into [TextFSM](https://github.com/google/textfsm/wiki/TextFSM) once again.  I had some experience with using TextFSM and Network-To-Code's [ntc-templates](https://github.com/networktocode/ntc-templates) module on Ansible and knew that it would be a good match for this job.  What TextFSM does well is allow you to use templates to parse text and make it into a structured python data structures like lists or dictionaries.  Network-to-Code works into this is because I already knew that they had a TextFSM template that worked for IOS/IOS-XE devices and the 'show ip route' command.  One good thing about relying on their template is that they have one of the biggest network automation user communities and if Cisco made some changes to a command output, usually someone would either fix the template or complain until others fixed it.

Therefore, the flow of my program ended up:
 1. Export from txt file to python string.
 2. Try to import pandas/textfsm and run advanced function.  If, this failed, just run a function that does the string count() method (and skip to print information).
 3. Parse string file with TextFSM template to make python list.
 4. Use list and template header information to make pandas dataframe.
 5. Remove duplicate network/mask combinations.
 6. Print information.


## ___Variable Naming/Program Structure___

This program uses the same variable naming, comment and program structure as last month's submission for, more information, see the section with the same name (Variable Naming/Program Structure) in the following link:
https://github.com/johnnywilkes/NPL_NOV_2018_TIME/blob/master/README.md


## ___Possible Refactoring/Feature Releases___

 - More testing template on a variety of different IOS/IOS-XE devices.
 - Make the same program to use on other platform routes such as NX-OS, ASA, etc.