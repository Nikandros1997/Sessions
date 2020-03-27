# Description:
This is an automation tool that was built with a goal in mind to store work sessions. As I am working in multiple projects at once (i.e. work, 2 different personal projects, etc), I find it very mundane and repetitive to open and close the different software I am using for each of my projects every time I need to work on it. With this command, it is possible to create multiple sessions and store all the apps related to each working session, automating the closing and opening of all the apps stored in it. Also, this command can be used in conjuction with the [Copy All Urls](https://chrome.google.com/webstore/detail/copy-all-urls/iiagcalhlpmgdipdcikkjiliaankcagj?hl=en) extension in Google Chrome to automatically store all the opened tabs and later automatically open them again, when the specific session is reloaded.

If you think something is missing from this command, have a look in my [to-dos](https://github.com/Nikandros1997/Sessions/projects/1) list to see if something similar to what you want is under development and if not give me your suggestions.

# How to copy all urls:
Google Chrome: [Copy All Urls](https://chrome.google.com/webstore/detail/copy-all-urls/iiagcalhlpmgdipdcikkjiliaankcagj?hl=en)  
Firefox: [Copy All Tab Urls](https://addons.mozilla.org/en-GB/firefox/addon/copy-all-tab-urls-we/)

# How to use the command:
sh session [options]  
**Currently, if you want to use the command, you have to go inside the folder and follow the instructions from there.**

# Options:
-**s** [name]                         -> saves a session with name [name]  
-**r** [name]                         -> reloads a session with name [name]  
-**i** [app_name] -**n** [session_name]   -> ignores from storing in sessions app with name [name], when no [name] is provided lists all running apps  
-**a**                                -> shows all running apps  
-**la**                               -> lists all active sessions  
