# -*- coding: utf-8 -*-

"""
This file is part of the **pyppeteer_sitecheck_scrapper**
project git@geodev.geo-instruments.com:DanEdens/pyppet_sitecheck_scrapper.git

:platform: Windows
:license:
:synopsis: This file removes non-human readable code from __main__
    It also provides a stable location to reference from various modules,
    as well as the below pre-defined values.
        Predefined Dates:
            today = datetime.utcnow()
            filedate = today.strftime("%Y-%m-%d")
            nowdate = today.strftime("%Y-%m-%d %H:%M:%S")
        Predefined Paths (str):
            ROOT_DIR: location of Scanner.py
            ROOT_data: Location of Chrome and Card-Generator Userdata

.. moduleauthor::  Dan Edens @DanEdens <Dan.Edens@geo-instruments.com>
"""

import ctypes
import os
from datetime import *

width = ctypes.windll.user32.GetSystemMetrics(0)
height = ctypes.windll.user32.GetSystemMetrics(1)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_data = ROOT_DIR+"\\data\\"
ROOT_card = ROOT_data+"cards\\"
today = datetime.utcnow()
nowdate = today.strftime("%Y-%m-%d %H:%M:%S")
filedate = today.strftime("%Y-%m-%d")
fileheader = 'Sitecheck Scan for: '+filedate+'\nProject: '
no_channel = (
    'Channel name does not match configured projects,\n'
    'Defaulting to test hook. View at the below url: \n'
    'https://webhook.site/#!/8a749da3-5b61-4060-b64f-22e3ae303f62/3542087d-0a3d-41af-811a-fb04f4c18b68/1'
)
uptoDate = 'Most recent data is within 24 hours\n'
outputfile = '_sitecheck.txt'
behindDate = 'Instrument is behind\n'
Warnfile = '_WatchdogFile.txt'
oldDate = 'Reading has been missing for over a week\n'
Oldfile = '_Watchdog_Old.txt'
loginmessage = 'Login Successful.'
scanplan = '\nScanning plan views:'
exit_message = 'Scan completed.'


class arg_text:
    """
    Text for --help
    """
    main = (
        'Automated Sitecheck scanner. \n'
        'Sensors are sorted into three categories:\n\n'
        'Up-to-date:    {0}' 
        'Overdue:       {1}' 
        'Old:           {2}\n'
        'Sensors that are behind are set up in an adaptive card and sent to the Regional Sitecheck channel of choice.\n'
        'To follow along with a browser in Evaluate mode, use flag --eval'.format(uptoDate, behindDate, oldDate)
    )
    old = (
        'Include sensors missing for Longer than a week. \n'
        'This is off by default to prevent unnecessary spam for known issues. \n'
        'It is assumed sensors missing for longer than 7 days have already been discussed.'
    )
    project = 'Define a single project to run.'
    watchdog = 'Set number of hours to mark as \'Up-to-date\' \n\'Old\' label is a 7 times multiple of this value'
    debug = 'Print verbose information about website navigation and browser events.'
    verbose = 'Print verbose information about senor status and data'
    weather = 'Include local weather data in status report.'
    eval = 'Shows a browser during scan to evaluate overdue sensors. '
    add_project = 'Interactive cli to configure a new project'
    edit_project = 'Opens projects file in editor.'
    plan = ''
    value = 'Include current Sensor data in report'
    time = 'Configure time to check against last update. Default is 24 hours'
    visual = (
        'Enables \'Headfull\' mode for Pyppeteer. \n'
        'This will create a visible browser, allowing the user to follow along with website navigation. \n'
        'This flag is intended for troubleshooting. Use --eval for an Interactive Scan using headfull mode'
    )
