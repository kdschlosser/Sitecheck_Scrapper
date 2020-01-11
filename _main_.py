#Daily Sitecheck Web Scrapper V. 4.0.0
import sys
import asyncio
import pathlib
import json
from pyppeteer import launch
from env import sites, text, creds

#temp for build
debug = 0
self = ''
watchdog = 86400000
watchlimit = watchdog * 7
user = 'dan.edens'
split = 'false'
#end temp


# print(obj[2])
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
        #check path exists
        streams = ''
        for x in path:
            print(x)
            streams += x
        return streams

class Report():
    def __init__(self, data):
        self.data = data
        
    def genCsv(self):
        pass

class Controller():
    def __init__(self, project):
        self.project = project
        pass

    async def filterSite(self):
        if self.project['hassite'] == 'amp':
            Controller.hasAmp(self)
        elif self.project['hassite'] == 'qv':
            Controller.hasQV(self)
        elif self.project['hassite'] == 'truelook': 
            Controller.hasTruelook(self)
            
            
    async def hasAmp(self):
        url = 'https://' + self.project + sites.selectors.amp.urlstring
        # verboselog('Url: ' + url)
        ampbuffer = await ampWebpage.Login(url, page)
        # await Debug.log(text.preloginmessage + project, Upfile)
        # await Debug.log(text.preloginmessage + project, Warnfile)
        # await Debug.log(text.preloginmessage + project, Oldfile)
        ampnavigate = await ampWebpage.gotoPlanview(url, planarray, Upfile, Oldfile, Warnfile, ampbuffer)
        await ampnavigate.close()
        return

    async def hasQV(self):
        namenum = projects[elem].proj
        qvbuffer = await qvWebpage.Login(page)
        # await Debug.log('\n' + text.postloginmessage, Upfile)
        # await Debug.log('\n' + text.postloginmessage, Warnfile)
        # await Debug.log('\n' + text.postloginmessage, Oldfile)
        qvproject = await qvWebpage.gotoProject(qvbuffer, namenum)
        # await Debug.log('\nProject Switched to ' + project, Upfile)
        # await Debug.log('\nProject Switched to ' + project, Warnfile)
        # await Debug.log('\nProject Switched to ' + project, Oldfile)
        qvscrape = await qvWebpage.gotoView(planarray, Upfile, Warnfile, Oldfile, qvproject)
        await qvscrape.close()
    
    async def hasTruelook(self):
        pass
    
class Ampadmin():
    def __init__(self, url, page):
        self.url = url
        self.page = page

    async def login(self):
        await self.page.goto(self.url)
        await self.page.type(sites.selectors.amp.logincss, creds.credentials.username)
        await self.page.type(sites.selectors.amp.pwcss, creds.credentials.password)
        await self.page.click(sites.selectors.amp.loginbutton)
        # await self.page.setViewport(width(1600) height(900))
        await self.page.waitFor(50)
        return self.page
  
#  Gives User directior to look for project.json
# projects = Config.loadProjects('dan.edens')
# print(projects)

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
        await self.page.type(sites.qv.logincss, creds.credentials.qvuser)
        await self.page.type(sites.qv.pwcss, creds.credentials.qvpass)
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
            txt =  await self.page.evaluate(link.innerHTML, link)
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
    projects = conFig.loadProjects(self, 'dan.edens')
    #projects = conFig.loadProjects(self, user) #production
    browser = await launch() #text.head
    k = 0
    for project in projects:
        print(project)
        #Need to add promise push here instead of on load page
        promises = []
        if project['skip'] != 'true':
            name = project['name']
            planarray = project['planarray']
            usercheckpath = '\\users\\'+ creds.credentials.user + '\\dailychecks\\' + text.filedate + '\\'
            pathlib.Path(usercheckpath).mkdir(parents=True, exist_ok=True)
            # await fs.promises.mkdir(usercheckpath, { recursive: true })
            pathtofile = usercheckpath + '_all'
            allpaths = [pathtofile+text.outputfile,pathtofile+text.pathtoOldfile,pathtofile+text.pathtoWarnfile]
            print(allpaths) 
            streams = await conFig.makeStream(self, allpaths)
            Upfile = streams[0] 
            Oldfile = streams[1] 
            Warnfile = streams[2]
            # page = await browser.newPage()
            # await Debug.log('Project:'+project+text.scanplan+planarray+'\n'+text.hasSitemessage + projects[elem]['hassite'] + '\n', Upfile)
            # await Debug.log('Project:'+project+text.scanplan+planarray+'\n'+text.hasSitemessage + projects[elem]['hassite'] + '\n', Warnfile)
            # await Debug.log('Project:'+project+text.scanplan+planarray+'\n'+text.hasSitemessage + projects[elem]['hassite'] + '\n', Oldfile)
            page = browser.newPage()
            promises.append(Controller.filterSite(page))
            # await Promise.all(promises)
    await browser.close()
    # groupend('Main')
    # if (verbose) {group('exitmsg')}
    print('\n' + text.exitmessage)
    # if (verbose) {groupend('exitmsg')}
    # if (preformance) {console.log(new Date().toISOString())}

    # browser = await launch(headless=False)
    # args: [`--window-size=${options.width},${options.height}`
    # page = await browser.newPage()
    # await page.goto('http://example.com')
    # await page.screenshot({'path': 'example.png'})

    # dimensions = await page.evaluate('''() => {
    #     return {
    #         width: document.documentElement.clientWidth,
    #         height: document.documentElement.clientHeight,
    #         deviceScaleFactor: window.devicePixelRatio,
    #     }
    # }''')

    # print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()
if __name__ == '__main__':
    pass
    asyncio.get_event_loop().run_until_complete(main()) #, debug=True