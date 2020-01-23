#Daily Sitecheck Web Scrapper V. 4.0.0
import sys
import io
import asyncio
import pathlib
import json
import datetime
import msvcrt as m
from io import StringIO
from pyppeteer import launch
from env import sites, text, creds
#pylint: disable=too-many-arguments
#temp for build
browser = launch({"headless": False})
debug = 0
verbose = True
getvalue = True
self = ''
watchdog = 86400000
watchlimit = watchdog * 7
user = 'dan.edens'
split = 'false'
#end temp

def wait():
    m.getch()

class Debug():
    def __init__(self, data, wfile):
        self.data = data
        self.wfile = 'notes.txt'
        # if not wfile:
        # else:
        #     self.wfile = wfile

    def log(self):
        if debug == 0:
            pass
        elif debug == 1:
            pass
        elif debug == 2:
            pass
        elif debug == 3:
            pass
        return

    def askQuestion(self, query):
        # readline.createInterface
        # input = process.stdin
        # output = process.stdout
        return

    def checkExists(self, file):
        pass

def loadProjects():
    with open('env/projects.json', 'r') as userdata:
        data=userdata.read()
        projects = json.loads(data)
        return projects

class processdata():
    def __init__(self, project):
        self.skip = project['skip']
        self.group = project['group']
        self.name = project['name']
        self.check = False
        self.proj = project['proj']
        self.planarray = project['planarray']
        self.hassite = project['hassite']

    def __repr__(self):
        return(self)


class conFig():
    def __init__ (self):
        pass

    async def makeStream(self, path):
        self.streams = {}
        self.count = 0
        for x in path:
            self.streams[self.count] = open(x, "a", encoding="utf-8")
            self.count += 1
            self.streams[self.count] = io.StringIO('temp newfile message.\n')
            self.count += 1
        return self.streams


def project_out_File(self):
    checkpath = '\\users\\'+ creds.user + '\\dailychecks\\' + text.filedate + '\\'
    pathlib.Path(checkpath).mkdir(parents=True, exist_ok=True)
    print(self.project.group)
    if self.project.group == True:
        output_pre = str(checkpath) + 'all_'
    else:
        output_pre = str(checkpath) + str(self.project.name) + '_'
    return [output_pre+text.outputfile, output_pre+text.Oldfile, output_pre+text.Warnfile]

class Report():
    def __init__(self, data):
        self.data = data

    def genCsv(self):
        pass

class Controller():
    async def __new__(self, project):
        project = processdata(project)
        self.project = project
        await self.EvalSite(self)

    async def EvalSite(self):
        if self.project.skip == 'true':
            print('Skipping project: '+ self.project.name)
        else:
            print('Running project: '+ self.project.name)  #remove later
            # allpaths = project_out_File(self)
            # self.project.streams = await conFig.makeStream(self, allpaths)
            print(text.fileheader)
            await self.filterSite(self)

    async def filterSite(self):
        if self.project.hassite == 'amp':
            await self.hasAmp(self)
        elif self.project.hassite == 'qv':
            await self.hasQV(self)

    async def hasAmp(self):
        self.url = 'https://' + self.project.name + '.geo-instruments.com/index.php'
        browser = await launch({"headless": False})
        self.page = await browser.newPage()
        await ampWebpage.Login(self)
        await self.page.waitFor(50)
        await ampWebpage.gotoPlanview(self)
        await self.page.waitFor(50)

        # await self.project.page.close()
        # return

    async def hasQV(self):
        self.project.page = await browser.newPage()
        # await qvWebpage.Login(self)
        await self.project.page.waitFor(50)
        # self.project.page = await qvWebpage.gotoProject(self)
        await self.project.page.waitFor(50)
        # self.project.page = await qvWebpage.gotoView(self)
        await self.project.page.waitFor(50)
        # await self.project.page.close()
        return


class ampWebpage():
    async def __init__(self):
        pass

    async def Login(self):
        await self.page.goto(self.url)
        await self.page.waitFor(500)
        await self.page.type(sites.amp.logincss, creds.username)
        # await self.page.waitFor(500)
        await self.page.type(sites.amp.pwcss, creds.password)
        # await self.page.waitFor(500)
        await self.page.click(sites.amp.loginbutton)
        # await self.page.waitFor(2000)
        return

    async def gotoPlanview(self): #url, planarray, Upfile, Oldfile, Warnfile, page):
        print(text.scanplan + self.project.planarray)
        planarray = self.project.planarray.split(",")
        for view in planarray:
            print(view)
            await self.page.goto(self.url + sites.amp.planview + view)
            for targetchild in text.sensorarray:
                self.targetchild = targetchild
                await ampWebpage.getLastupdate(self)


    async def getLastupdate(self): #, Upfile, Oldfile, Warnfile, page):
        for typeofsensorbox in sites.amp.label:
            namesel = str('body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + self.targetchild + sites.amp.title)
            valuesel = str('body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + self.targetchild + sites.amp.sensor)
            name = await self.page.J(namesel)
            link = await self.page.J(valuesel)
            if name == None:
                pass
            else:
                sensor =  await self.page.evaluate('(name) => name.textContent', name)
                value =  await self.page.evaluate('(link) => link.textContent', link)
                date = await self.page.evaluate('(link) => link.title', link)
                print(sensor, value)
                data = '\nSensor name: ' + sensor
                data += '\nLast Updated on AMP: '
                if getvalue:
                    data += '\nCurrent value: ' + value

                # TODO pdate = datetime.parse(date)
                # pnowdate = datetime.parse(text.nowdate)
                # diff = pnowdate - pdate
                diff = 10000
                if diff <= watchdog:
                    data += date
                    if verbose:
                        data += '\n' + text.uptoDate
                    print(data)
                elif diff >= watchdog & diff <= watchlimit:
                    data += date
                    if verbose:
                        data += '\n' + text.behindDate
                    print(data)
                else:
                    data += date
                    if verbose:
                        data += '\n' + text.oldDate
                    print(data)

            # except:
            #     print('Caught:')
            #     pass
            #     await Debug.askQuestion(self, 'Will cont when ready')


class qvWebpage():
    def __init__(self, project):
        self.page = project.page
        self.planarray = project.planarray
        self.namenum = project.namenum
        self.Upfile = project.Upfile
        self.Warnfile = project.Warnfile
        self.Oldfile = project.Oldfile
        self.project = project
        self.check = project.check
        self.url = project.url
        self.planarray = project.planarray


    async def Login(self):
        try:
            await self.page.goto(sites.qv.urlstring)
        except: #ERR_ADDRESS_UNREACHABLE
            print('url error')
        await self.page.type(sites.qv.logincss, creds.qvuser)
        await self.page.waitFor(300)
        await self.page.type(sites.qv.pwcss, creds.qvpass)
        await self.page.waitFor(300)
        await self.page.click(sites.qv.loginbutton)
        # await self.page.setViewport(width: 1600, height: 900)
        await self.page.waitFor(2000)
        return self.page

    async def gotoProject(self):
        await self.page.click(sites.qv.menuprojects)
        await self.page.waitFor(200)
        await self.page.hover(sites.qv.scrollbar)
        await self.page.waitFor(500)
        await self.page.click(sites.qv.Qvprojectpre + self.namenum + sites.qv.Qvprojectpost)
        await self.page.waitFor(500)
        return self.page


    async def gotoView(self):
        for view in self.planarray:
            if view != '0':
                await self.page.click(sites.qv.views)
                await self.page.waitFor(500)
                await self.page.hover(sites.qv.scrollbar2)
                await self.page.waitFor(200)
                await self.page.click(sites.qv.thumb+view)
            else:
                pass

            await self.page.waitFor(1000)
            for targetchild in text.sensorarray:
                await qvWebpage.getLastupdate(self, targetchild)

            return self.page


    async def getLastupdate(self, targetchild):
        sensor = '#objects > img:nth-child(' + targetchild + ')'
        try:
            await self.page.hover(sensor)
            link = await self.page.querySelector(sites.qv.hoverbox)
            txt =  await self.page.evaluate('(link) => link.innerHTML', link)
            spltd = txt.split('<br>')
            data = '\nSensor name: ' + spltd[0]
            date = spltd[3].split("data: ").pop()
            # await Debug.log(data + ' \nDate:\n' + date + '\n', Upfile)
            pdate = '' #Date.parse(date)
            pnowdate = '' #Date.parse(text.nowdate)
            diff = pnowdate - pdate
            if diff <= watchdog:
                data += date
                # if verbose:
                #     data += '\n' + text.uptoDate
                # await Debug.log(data, Upfile)
            elif diff >= watchdog and diff <= watchlimit:
                data += date
                # if verbose:
                #     data += '\n' + text.behindDate
                # await Debug.log(data, Warnfile)
            else:
                data += date
                # if verbose:
                #     data += '\n' + text.oldDate

                # await Debug.log(data, Oldfile)
        except: #(UnhandledPromiseRejectionWarning):
            pass
        return

async def main():
    #Returns List of project configs {[project],[project],[project]}
    projects = loadProjects()
    futures = [await (Controller(project)) for project in projects]
    # await asyncio.gather(*futures)
    await browser.close()

# If run occurs from directly running the program
if __name__ == '__main__':
    run = asyncio.run(main())
    print('\n' + text.exitmessage)