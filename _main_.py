#Daily Sitecheck Web Scrapper V. 4.0.0
import sys
import io
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
        streams = {}
        count = 0
        for x in path:
            streams[count] = io.StringIO('temp newfile message.\n')
            count += 1
        # print(streams)
        return streams

    def groupFile(self, usercheckpath, project):
        pathlib.Path(usercheckpath).mkdir(parents=True, exist_ok=True)
        if project['group'] == 'true':
            c = str(usercheckpath) + 'all_'
        else:
            c = str(usercheckpath) + str(project['name']) + '_'
        return c

class Report():
    def __init__(self, data):
        self.data = data
        
    def genCsv(self):
        pass

class Controller():
    def __init__(self, project):
        self.project = project

    async def filterSite(self):
        if self.project['hassite'] == 'amp':
            Controller.hasAmp(self)
        elif self.project['hassite'] == 'qv':
            Controller.hasQV(self)
        elif self.project['hassite'] == 'truelook': 
            Controller.hasTruelook(self)
            
            
    async def hasAmp(self):
        url = 'https://' + self.project + sites.selectors.amp.urlstring
        ampbuffer = await ampWebpage.Login(self, url)
        
        # ampnavigate = await ampWebpage.gotoPlanview(url, planarray, Upfile, Oldfile, Warnfile, ampbuffer)
        await ampnavigate.close()
        return

    # should the site runs themselves be static to ensure data is logged in order?
    async def hasQV(self):
        namenum = self.project['proj']
        qvbuffer = await qvWebpage.Login(self.page)
        qvproject = await qvWebpage.gotoProject(qvbuffer, namenum)
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
class ampWebpage():
    def __init__(self, page):
        self.page = page
        pass
    
    async def Login(self):
        try:
            await self.page.goto(url)
        except(ERR_ADDRESS_UNREACHABLE): 
            print('url error')
        await self.page.type(sites.selectors.amp.logincss, creds.username)
        await self.page.type(sites.selectors.amp.pwcss, creds.password)
        await self.page.click(sites.selectors.amp.loginbutton)
        # await self.page.setViewport({ width: 1600, height: 900 })
        await self.page.waitFor(50)
        return self.page

    async def gotoPlanview(self): #url, planarray, Upfile, Oldfile, Warnfile, page):
        for view in self.planarray:
            group('Planview ' + view)
            if check: 
               ans = await Debug.askQuestion("Check over Planview?\nNote:\n").then(Debug.print(ans))
            await Debug.print(text.loginmessage + view + '\nUrl:' + url + sites.selectors.amp.planview + view, Upfile)
            await Debug.print(text.loginmessage + view + '\nUrl:' + url + sites.selectors.amp.planview + view, Warnfile)
            await Debug.print(text.loginmessage + view + '\nUrl:' + url + sites.selectors.amp.planview + view, Oldfile)
            await page.goto(url + sites.selectors.amp.planview + view)
            for targetchild in text.sensorarray:
                await ampWebpage.getLastupdate(targetchild, Upfile, Oldfile, Warnfile, page)}
            groupend('Planview')
        }
        return page
    }

    async def getLastupdate(self, targetchild): #, Upfile, Oldfile, Warnfile, page):
        for typeofsensorbox in sites.selectors.amp.label:
            namesel = 'body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + targetchild + sites.selectors.amp.title
            valuesel = 'body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + targetchild + sites.selectors.amp.sensor
                name = await page.querySelector(namesel)
                link = await page.querySelector(valuesel)
            try:
                sensor =  await page.evaluate(name.textContent, name)
                value =  await page.evaluate(link.textContent, link)
                date = await page.evaluate(link.title, link)
                group('Sensor: ' + targetchild)
                data = '\nSensor name: ' + sensor
                data += '\nLast Updated on AMP: '
                if getvalue:
                    data += '\nCurrent value: ' + value
                
                pdate = Date.parse(date)
                pnowdate = Date.parse(text.nowdate)
                diff = Math.abs(pnowdate - pdate)
                if (diff < watchdog :
                    data += date
                    if (verbose:data += '\n' + text.uptoDate}
                    await Debug.print(data, Upfile)
                } else if (diff > watchdog & diff < watchlimit:
                    data += date
                    if (verbose:data += '\n' + text.behindDate}
                    await Debug.print(data, Warnfile)
                } else {
                    data += date
                    if (verbose:data += '\n' + text.oldDate}
                    await Debug.print(data, Oldfile)
                }
                groupend('Sensor: ' + targetchild)
            }
            except(error:
                exception = error.message.split(':')
                if (exception[0] = 'No node found for selector':
                } else if (exception[0] = 'Evaluation failed':
                } else if (exception[0] = 'UnhandledPromiseRejectionWarning':
                } else {
                    console.log('Caught:', error.message)
                    await Debug.askQuestion('Will cont when ready')}
                }
        }
            return page
    }
}


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
        # print(project)
        #Need to add promise push here instead in on load page
        promises = []
        if project['skip'] != 'true':
            usercheckpath = '\\users\\'+ creds.credentials.user + '\\dailychecks\\' + text.filedate + '\\'
            pathtofile = conFig.groupFile(self, usercheckpath, project)
            allpaths = [pathtofile+text.outputfile, pathtofile+text.pathtoOldfile, pathtofile+text.pathtoWarnfile]
            # print(allpaths[0])             
            project['streams'] = await conFig.makeStream(self, allpaths)
            # print(project['streams'])
            project['page'] = browser.newPage()
            promises.append(Controller(project))
        await promises
    print('\n' + text.exitmessage)
    await browser.close()
if __name__ == '__main__':
    pass
    asyncio.get_event_loop().run_until_complete(main()) #, debug=True