 
![](docs/logo-graphic.png)  
# Daily Site-check Scanner  
#### Intended for Geo-Instruments Internal use only.

---

This tool is designed to scan client project sites, providing convenient
and interactive assistance to field technicians.

Makes use of Pyppeteer, a [Python port](https://miyakogi.github.io/pyppeteer/index.html) of Google's Headless browser automation library, [Puppeteer](https://pptr.dev/)  
If interested, you can [try it out here](https://try-puppeteer.appspot.com/_) or install with pip.
```
python3 -m pip install pyppeteer
```
# The Why
This is largely a convenience tool, an automated approach to what AmpAdmin already provides for Amp projects.
Built with flexibility in mind as our platform pool contuines to grow.

```
This is not intended to replace use of the built-in watchdog alarms,  
Nor would I suggest shying away from checking over the sites manually.
The goal is to be able to bring items to the attention of Apps 
```

##  The benefits of this method are intended as the following:
1. Check if data is visible from the clients perspective.
The final version will compare data gathered using both Admin and User credentials.

2. Convenient information cards provided to teams for field tech convienence
Checking websites manually in the field can lead to missing warning flags when they appear.
I hope to use Power Automate's AI builder for data trend detections and predictions in later verions

3. Provide a convenient overview product to region managers.
After a daily check-in time, Region channels can be sent a status report detailing their tech's confirmations.
Deliverable to the team channel or through a Flowbot private message.
Currently planned card button options include:
    1. Project summary and missing list
    2. Lightweight update of which projects have been marked confirmed.
    3. Retrieve weekly PDF report

4. Supports Quickview, Truelook, and weather reports.

Sensors status is rated as one of these three categories:
```
1. Up-to-date:         Timestamp is within 24 hours.
2. Warning list:     Timestamp is older than 24 hours.
3. Old list:         Timestamp is older than a week.
```

Card delivery is currently focused at Regional Sitecheck channels.
Another availble option is to send to a private chat channel per tech.


MileStones and Issues
---

[Optimization](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/-/milestones/5) and [Documentation](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/37) update.  
    
 1. Finish [Label refactoring and version](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/34) tagging  
 2. Finish [docstring]((https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/9)) and type hints  
 3. Finish creating [Project Documents and API reference](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/17) 
 4. [Tree shake](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/11) variables  

Build Module for version [Release v1.0.0](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/-/milestones/8)

 1. Create [build script](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/15)
 2. Build [config manager](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/38) for setting up userdata
 3. Build [Error handler](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/39)
 4. Build [Docker](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/36) image
 5. Generate End user [package](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/16)

[Adaptive card](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/-/milestones/15) Template upate.

 1. Integrate ['Get-Value' option](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/32)
 3. Cosmetic overhaul of Cards.

Interactive mode.  

 1. Build [Cli module](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/40)  
 2. Re-apply [system arguments](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/44)
 3. Directed checks on single projects or plan views.  
 2. Build and Integrate [Weather module](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/42)

Build [Check mode](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/-/milestones/9).
 
 1. Headfull navigation that prompts user input on [Watchdog event](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/25).
 2. Choose an option for [overlaying information](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/27) onto project site.
 3. Intergrate Screenshot support
 4. Intergrate card preview sdk

Build backend of ['Power Automate'](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/-/milestones/14) controller

 1. Build response listener  
 2. Convert local generator to Flow template generator  
 3. Create framework for [Manager update](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/-/milestones/14) card  

Testing

 1. Alpha Test - Delivery automated cards for personal projects for 14 day
    contiguous period
 2. [Run](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper/issues/36) error trials with findings and add all possible exception handles
 3. Run beta with non-code savy techs




