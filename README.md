![](Documentation/email-signature-graphic176.png)
# Daily Site-check Scanner
### This tool is designed for Geo-Instruments Internal use only.
---

This tool is designed to scan client project sites and provide convenient
and interactive assistance to field technicans.

To accomplish this, It makes use of Pyppeteer, a [Python port](https://miyakogi.github.io/pyppeteer/index.html) of Google's Headless browser automation library [Puppeteer](https://pptr.dev/)
If interested, you can [try it out here](https://try-puppeteer.appspot.com/_) or by running:
```
python3 -m pip install pyppeteer
```
# The Why
This is largely a convience tool, an automated approach to what AmpAdmin already provides,
Built for flexabilty as our platform pool contuines to grow.

```
This is not intended to replace the built-in watchdog alarms, nor do I suggest shying away from checking over the sites manually.
```


##  The benefits of this method are intended as the following:
1. Check if data is visible from the clients perspective.
The final version will compare data gathered using both Admin and User credentials.

2. Convient infomation cards provided to teams for field tech convienence
Checking websites manually in the field can lead to missing warning flags when they appear.
I hope to use Power Automate's AI builder for data trend detections and predictions in later verions

3. Provide a convient overview product to region managers.
After a daily check-in time, Region channels can be sent a status report,
optionally delieved to the team channel or through a Flowbot private message.
Currently planned options include:
    1. per-project missing sensors list
    2. more lightweight update of which projects have been checked.

4. Supports Quickview, Truelook, and weather reports.

Sensors status is rated as one of these three categories:
```
1. Up-to-date: 		Timestamp is within 24 hours.
2. Warning list: 	Timestamp is older than 24 hours.
3. Old list: 		Timestamp is older than a week.
```

Card delivery is currently focused at Regional Sitecheck channels.
Another availble option is to send to a private chat channel per tech.

# Known Issues and Critical missing features:
```
QV side panels longer than window size currently not supported (Only known case is The Vegas project)
```
---
## TODO:
```
1. Finish Optimization and documentation update.
	1. Finish Refactoring style
    2. Finish docstring and type hinting
	3. Finish creating Project Documents and API refrence
	4. Tree shake variables
```
```
2. Finish dev build script.
	1. Create 1 click development install
	2. Build config manager for setting up userdata
    3. Build Bug report handler and Feedback form
	3. Generate Enduser package
```
```
3. Build check mode.
	1. Headfull navigation that prompts user input on Watchdog event.
	2. Choose an option for overlaying information onto project site.
    3. Intergrate Screenshot support
	4. Intergrate card preview sdk
```
```
4. Rebuild Team's card.
    1. Cosmetic overhaul of Cards.
    . Intergrate Sensor value data

    . Intergrate Weather data

```
```
5. Interactive mode.
	1. Build Cli module
    2. Re-apply previously availble command line args
    3. Directed checks on single projects or plan views.
    4. Screenshots through SMS
    5. Command line compatiable classes
    6.
```
```
6. Build Power_Automate backend controller
	1. Build response listener
    2. Convert local generator to Flow template generator
	3. Create framework for Manager update card
```

```
6. Testing
    1. Alpha Test period completed - Delivery automated cards for personal projects for 14 day
       contiguous period
    2. Run forced error trials with findings and add all possible exception handles
    3. Run beta with non-code savy techs
```
---
# Completed Milestones
1. Functional version of Amp scanner and QV scanner have been built in both Nodejs and Python.
    Intially the project sololy utlizied NodeJS and Puppeteer,  converted once I realized it had potential to be used by other techs.

The following websites have been successfully scanned and output data in Team's card format:
```
Captiolcomplex, AudicentralHouston, 425Riverside, Unioncityintermodal, Redbeach, Santabarbaratjwall, Beverlyhillshigh, Isabelladam, 755fig, Haieng, Tesolongbeach8485, Natoma, Harbour Bridge, TarzanaMed, texasinternational, and Sherridan Hills
```
Cards have been successfully recieved on Teams.
