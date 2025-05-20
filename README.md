AtomicNWS -- NWS/NOAA Weather Receiver Software from the Atomic Corporation
=================================================================

This program is a light-weight Python based weather alert receiver that pulls directly from Weather.gov (The National Weather Service / NOAA).
It's based off an SDK that wraps the NWS/NOAA API. Settings are available to specify what alerts you want to be notified of,
as well as to enable logging and alert sounds for emergency alerts. Default alerts are for tornado watches, warnings and emergencies, severe thunderstorm warnings, and hurricane warnings.

If sounds are enabled, EAS SAME tones will be played. They are loud.

The time range is specified in settings.txt as time_within. The default is 30 minutes.
States can also be specified in settings.txt. Two letter code(s) must be used specified: ("CA") or ("MO, IL, KS") .
If no state is specified (i.e state = ""), it will search nationwide for alerts.

The software runs without a UI, directly through the Terminal/Console. 
A UI will most likely not be implimented, as information can be clearly displayed through the console.

When editing settings.txt, do not delete quotation marks ("") -- edit the data between them.

-------------------------------------------
INSTALLATION FOR WINDOWS BASED MACHINES:
===============

0. Download the AtomicNWS.zip file from GitHub

1. Extract the AtomicNWS folder from the downloaded zip file.

2. Run "AtomicNWS.exe"

INSTALLATION FOR LINUX/MAC/UNIX BASED MACHINES:
==================================

0. Download the AtomicNWS.zip file from GitHub

1. Extract the AtomicNWS folder from the downloaded zip file.

2. Through the Terminal, CD to the AtomicNWS folder.

3. Open InstallerPackage.sh through the Terminal by running the command "./InstallerPackage.sh" (without quotes) -- this will install the program's dependencies.

3.1. (OR) Run the program through Terminal directly. -- CD to the folder, and type "python3 AtomicNWS.py" (without quotes)

4. Open UpdatePackage.sh through the Terminal by running the command "./UpdatePackage.sh" (without quotes) -- this will update dependencies (if there is an update)

5. Double click the "run.sh" file, and select "Run in Terminal".

-----------------------------------------------

Closing Statement:
============

This program is Open-Source. You are free to make any and all modifications to this program as desired. If you have a fix or an improvement that you made, and would like to have it added, let me know.

This program was made by using existing libraries and modules found on GitHub or PyPi. Credit for usage of these goes back to their respective owners.

As of 5/19/2025, "Atomic Incorporated" does not exist (at least under me). There are no copyright holders. I do not have a copyright on this program. The name is for visuals exclusively.

https://www.atomiccorp.org/
