"""
    This file removes non-human readable code from __main__
    It also provides a stable location to reference from various modules,
    as well as the below pre-defined values.
        Predefined Dates:
            today = datetime.utcnow()
            filedate = today.strftime("%Y-%m-%d")
            nowdate = today.strftime("%Y-%m-%d %H:%M:%S")
        Predefined Paths (str):
            ROOT_DIR: location of Scanner.py
            ROOT_data: Location of Chrome and Card-Generator Userdata
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
no_channel = 'Channel name does not match configured projects,\nDefaulting to test hook. View at the below url: \nhttps://webhook.site/#!/8a749da3-5b61-4060-b64f-22e3ae303f62/3542087d-0a3d-41af-811a-fb04f4c18b68/1'
uptoDate = 'Most recent data is within 24 hours\n'
outputfile = '_sitecheck.txt'
behindDate = 'Instrument is behind\n'
Warnfile = '_WatchdogFile.txt'
oldDate = 'Reading has been missing for over a week\n'
Oldfile = '_Watchdog_Old.txt'
loginmessage = 'Login Successful.'
scanplan = '\nScanning plan views:'
exit_message = 'Scan completed.'


class Options:
    headless = False
    chrome_args = ['--start-maximized', ' --user-data-dir='+ROOT_data]
    verbose = True
    getvalue = True
    watchdog = 86400
    watch_limit = watchdog * 7


class arg_text:
    """
        Text for --help
    """
    watchdog = 'None'
    main = 'Automated Sitecheck scanner'
    debug = 'Print verbose information about website navigation and browser events.'
    verbose = 'Print verbose information about senor status and data'
    weather = 'Include local weather data in status report'
    eval = 'Shows a browser during scan to evaluate overdue sensors. '
    usage = ''
    add_project = 'Interactive cli to configure a new project'
    edit_project = 'Interactive cli to edit a projects configuration'
    plan = ''
    get_value = ''
    time = 'Configure time to check against last update. Default is 24 hours'
    visual = '--disable-headless enables \'Headfull\' mode for Pyppeteer. \nThis will create a visible browser, allowing the user to follow along with website navigation. \nThis flag is intended for troubleshooting. Use --eval for an Interactive Scan using headfull mode'
