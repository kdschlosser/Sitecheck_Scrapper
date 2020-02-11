debug = 0
import ctypes
import os
import sys
from datetime import *

from dateutil.parser import *

width = ctypes.windll.user32.GetSystemMetrics(0)
height = ctypes.windll.user32.GetSystemMetrics(1)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_data = ROOT_DIR + "\\data\\"
now = parse("Sat Oct 11 17:13:46 UTC 2003")
today = datetime.utcnow()
nowdate = today.strftime("%Y-%m-%d %H:%M:%S")
filedate = today.strftime("%Y-%m-%d")
pathtonote = os.path.abspath(os.path.dirname(sys.argv[0])) + '/_' + filedate + '/Notes.txt'

fileheader = 'Sitecheck Scan for: ' + filedate + '\nProject: '
no_channel = 'Channel name does not match configured projects,\nDefaulting to test hook. View at the below url: \nhttps://webhook.site/#!/8a749da3-5b61-4060-b64f-22e3ae303f62/3542087d-0a3d-41af-811a-fb04f4c18b68/1'
outputfile = '_sitecheck.txt'
Warnfile = '_WatchdogFile.txt'
Oldfile = '_Watchdog_Old.txt'
uptoDate = 'Most recent data is within 24 hours\n'
behindDate = 'Instrument is behind\n'
oldDate = 'Reading has been missing for over a week\n'
scanplan = '\nScanning plan views:'
postloginmessage = 'Login Successful.'
usage_argdesc = 'Usage: --debug=[1,2,3] -p <project> -o %date_<filename>.txt'
help_argdesc = ''
version_argdesc = 'Version: '
project_argdesc = 'project=<projectname> Project to scan'
output_argdesc = "output=<_filename.txt> output file name. \nOutput file Default value is: \'_sitecheck.txt\'"
setup_argdesc = 'Input project name from the Amp URL. <--projectname=newtreehouse> <--other options to add later when i make generator>'
debug_argdesc = 'Run tests without web requests and redirect from file output to console.'
watchlisttxt = "Watchdog alert list:\n"
oldlisttxt = "Watchdog alert items older than a week:\n"
filerefreshed = 'Creating File...'
