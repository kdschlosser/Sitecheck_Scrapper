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

#temp for build
debug = 0
verbose = True
getvalue = True
self = ''
watchdog = 86400000
watchlimit = watchdog * 7
user = 'dan.edens'
split = 'false'
#end temp


async def get_page(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    return page


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
        # self.user = user
        # self.path = path

    async def makeStream(self, path):
        streams = {}
        count = 0
        for x in path:
            # print(x)
            streams[count] = open(x, "a", encoding="utf-8")
            count += 1
            streams[count] = io.StringIO('temp newfile message.\n')
            count += 1
        # print(streams)
        return streams


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
    async def __new__(self, browser, project):
        project = processdata(project)
        self.project = project
        self.browser = browser
        await self.EvalSite(self)

    async def EvalSite(self):
        if self.project.skip == 'true':
            print('Skipping project: '+ self.project.name)
        else:
            print('Running project: '+ self.project.name)  #remove later
            allpaths = project_out_File(self)
            self.project.streams = await conFig.makeStream(self, allpaths)
            await filterSite(self)

async def filterSite(self):
    if self.project.hassite == 'amp':
        await Has_Site.hasAmp(self)
    elif self.project.hassite == 'qv':
        await Has_Site.hasQV(self)

class Has_Site():
    async def hasAmp(self):
        self.project.url = 'https://' + self.project.name + '.geo-instruments.com/index.php'
        self.project.page = await self.browser.newPage()
        # await ampWebpage.Login(self)
        await self.project.page.waitFor(50)
        # await ampWebpage.gotoPlanview(self)
        await self.project.page.waitFor(50)
        # await self.project.page.close()
        return

    async def hasQV(self):
        self.project.page = await self.browser.newPage()
        # await qvWebpage.Login(self)
        await self.project.page.waitFor(50)
        # self.project.page = await qvWebpage.gotoProject(self)
        await self.project.page.waitFor(50)
        # self.project.page = await qvWebpage.gotoView(self)
        await self.project.page.waitFor(50)
        # await self.project.page.close()
        return


class Ampadmin():
    def __init__(self, url, page):
        self.url = url
        self.page = page

    async def login(self):
        await self.page.goto(self.url)
        await self.page.type(sites.amp.logincss, creds.username)
        await self.page.type(sites.amp.pwcss, creds.password)
        await self.page.click(sites.amp.loginbutton)
        # await self.page.setViewport(width(1600) height(900))
        await self.page.waitFor(50)
        return self.page

class ampWebpage():
    async def __init__(self, browser, project):
        self.planarray = project.planarray
        self.namenum = project.namenum
        self.Upfile = project.Upfile
        self.Warnfile = project.Warnfile
        self.Oldfile = project.Oldfile
        self.project = project
        self.check = project.check
        self.url = project.url
        self.planarray = project.planarray
        self.page = project.page



    async def Login(self, browser, project):
        await project.page.goto(project.url)
        await project.page.waitFor(300)
        await project.page.type(sites.amp.logincss, creds.username)
        await project.page.waitFor(300)
        await project.page.type(sites.amp.pwcss, creds.password)
        await project.page.waitFor(300)
        await project.page.click(sites.amp.loginbutton)
        await project.page.waitFor(2000)
        return project.page

    async def gotoPlanview(self): #url, planarray, Upfile, Oldfile, Warnfile, page):
        print(self.planarray)
        for view in self.planarray:
            print(view)
            # if self.check:
            #    ans = await Debug.askQuestion(self, "Check over Planview?\nNote:\n").then(Debug.log(ans))
            await self.page.goto(self.url + sites.amp.planview + view)
            for targetchild in text.sensorarray:
                await ampWebpage.getLastupdate(self, targetchild)


    async def getLastupdate(self, targetchild): #, Upfile, Oldfile, Warnfile, page):
        for typeofsensorbox in sites.amp.label:
            namesel = str('body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + targetchild + sites.amp.title)
            valuesel = str('body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + targetchild + sites.amp.sensor)
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
    #Creates Initial browser context
    browser = await launch({"headless": False})

    futures = [(Controller(project, browser)) for project in projects]
    asyncio.gather(*futures)
    # await browser.close()

# If run occurs from directly running the program
if __name__ == '__main__':
    run = asyncio.run(main())
    print('\n' + text.exitmessage)