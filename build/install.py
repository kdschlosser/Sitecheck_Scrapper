import os,sys

folderPath = ''
APP_NAME = 'SitecheckScanner'


def UpdateStartupShortcut(create):
    path = os.path.join(folderPath.Startup, APP_NAME+".lnk")

    if os.path.exists(path):
        os.remove(path)

    if create:
        if not os.path.exists(folderPath.Startup):
            os.makedirs(folderPath.Startup)

        Shortcut.Create(path=path, target=os.path.abspath(sys.executable), arguments="-h -e OnInitAfterBoot",
                startIn=os.path.dirname(os.path.abspath(sys.executable)), )
