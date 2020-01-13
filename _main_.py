#Daily Sitecheck Web Scrapper V. 4.0.0
import sys
import io
import asyncio
import pathlib
import json
import datetime
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

async def get_browser():
    return await launch({"headless": False})

async def get_page(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    return page

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

class data:
    #parse json dict into object
    def __init__(self, project):
        self.skip = project['skip']
        self.group = project['group']
        self.name = project['name']
        self.check = False
        self.proj = project['proj']
        self.planarray = project['planarray']
        self.hassite = project['hassite']
        return

class conFig():
    def __init__ (self):
        pass
        # self.user = user
        # self.path = path
    
    def loadProjects(self, user): 
        with open('env/projects.json', 'r') as userdata:
            data=userdata.read()
            projectlist = json.loads(data)
            return projectlist

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

    def groupFile(self, usercheckpath, project):
        pathlib.Path(usercheckpath).mkdir(parents=True, exist_ok=True)
        if project.group == True: 
            c = str(usercheckpath) + 'all_'
        else:
            c = str(usercheckpath) + str(project.name) + '_'
        return c

class Report():
    def __init__(self, data):
        self.data = data
        
    def genCsv(self):
        pass

class Controller():
    def __init__(self, project):
        # self.page = ''
        self.name = project.name
        # self.project = project
    
    async def filterSite(self, project):
        if project.hassite == 'amp':
            print (project.page)
            await Controller.hasAmp(self, project)
        elif project.hassite == 'qv':
            pass
            # Controller.hasQV(self, project)
        elif project.hassite == 'truelook': 
            Controller.hasTruelook(self, project)
            
            
    async def hasAmp(self, project):
        project.url = 'https://' + project.name + sites.amp.urlstring
        project.page = await ampWebpage.Login(project)
        await project.page.waitFor(50)
        project.page = await ampWebpage.gotoPlanview(project)
        await project.page.waitFor(50)
        await project.page.close()
        return

    def hasQV(self, project):
        project.page = await qvWebpage.Login(project)
        await project.page.waitFor(50)
        project.page = await qvWebpage.gotoProject(project)
        await project.page.waitFor(50)
        project.page = await qvWebpage.gotoView(project)
        await project.page.waitFor(50)
        await project.page.close()
    
    def hasTruelook(self, project):
        pass
    
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
  
#  Gives User directior to look for project.json
# projects = Config.loadProjects('dan.edens')
# print(projects)
class ampWebpage():
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
            await self.page.goto(self.url)
        except: # ERR_ADDRESS_UNREACHABLE: 
            print('url error')
        await self.page.waitFor(300)
        await self.page.type(sites.amp.logincss, creds.username)
        await self.page.waitFor(300)
        await self.page.type(sites.amp.pwcss, creds.password)
        await self.page.waitFor(300)
        await self.page.click(sites.amp.loginbutton)
        await self.page.waitFor(300)
        return self.page

    async def gotoPlanview(self): #url, planarray, Upfile, Oldfile, Warnfile, page):
        for view in self.planarray:
            if self.check: 
               ans = await Debug.askQuestion(self, "Check over Planview?\nNote:\n").then(Debug.log(ans))
            await self.page.goto(self.url + sites.amp.planview + view)
            for targetchild in text.sensorarray:
                await ampWebpage.getLastupdate(self, targetchild)
        return self.page

    async def getLastupdate(self, targetchild): #, Upfile, Oldfile, Warnfile, page):
        for typeofsensorbox in sites.amp.label:
            namesel = str('body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + targetchild + sites.amp.title)
            valuesel = str('body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + targetchild + sites.amp.sensor)
            name = await self.page.J(namesel)
            link = await self.page.J(valuesel)
            if name == None:
                pass
            else: 
                # print(link)        
            # try:
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
        return self.page


class qvWebpage():
    def __init__(self, page, planarray, namenum, Upfile, Warnfile, Oldfile):
        self.page = page
        self.planarray = planarray
        self.namenum = namenum
        self.Upfile = Upfile
        self.Warnfile = Warnfile
        self.Oldfile = Oldfile

    
    async def Login(self):
        try:
            await self.page.goto(sites.qv.urlstring)
        except: #ERR_ADDRESS_UNREACHABLE
            print('url error')
        await self.page.type(sites.qv.logincss, creds.qvuser)
        await self.page.type(sites.qv.pwcss, creds.qvpass)
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
            # loginmsg = text.loginmessage + view
            # await Debug.log(loginmsg, self.Upfile)
            # await Debug.log(loginmsg, self.Warnfile)
            # await Debug.log(loginmsg, self.Oldfile)
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
    # Retrieves list of projects from Json file as 'projects'
    projects = conFig.loadProjects(self, 'dan.edens') 
    
    # Creates browser
    browser = await get_browser() #text.head
    
    #cycles through each project as 'project'
    for each in projects:
        project = data(each)
        # print(project.skip)
        # TODO Need to add promise push here instead in on load page
        if project.skip != 'true':
            print(project)
            checkpath = '\\users\\'+ creds.user + '\\dailychecks\\' + text.filedate + '\\'
            pre_ = conFig.groupFile(self, checkpath, project)
            allpaths = [pre_+text.outputfile, pre_+text.Oldfile, pre_+text.Warnfile]
            project.streams = await conFig.makeStream(self, allpaths)
            project.page = await browser.newPage()
            print(project.name)
            await Controller.filterSite(self, project)
    await browser.close()

if __name__ == '__main__':
    pass
    run = asyncio.get_event_loop().run_until_complete(main()) #, debug=True
    # run.close()
    print('\n' + text.exitmessage)