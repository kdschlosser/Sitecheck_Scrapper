#Daily Sitecheck Web Scrapper V. 4.0.0
import sys
import asyncio
import json
from pyppeteer import launch
from env import sites, text, creds

#temp for build
debug = 0
self = ''
watchdog = 86400000
watchlimit = watchdog * 7
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
        
class Config():
    def __init__ (self, user, path):
        self.user = user
        self.path = path

    def loadProjects (self): 
        #proj = __dirname + '/users/'+user+'/projects.json'
        with open('env/projects.json', 'r') as userdata:
            data=userdata.read()
            projectlist = json.loads(data)
            return projectlist

    def makeStream(self):
        #check path exists
        for x in self.path:
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
        pass
    
    async def hasAmp(self):
        url = 'https://' + project + LOCAL.amp.urlstring
        # verboselog('Url: ' + url)
        ampbuffer = await ampWebpage.Login(url, page)
        # await Debug.print(text.preloginmessage + project, Upfile)
        # await Debug.print(text.preloginmessage + project, Warnfile)
        # await Debug.print(text.preloginmessage + project, Oldfile)
        ampnavigate = await ampWebpage.gotoPlanview(url, planarray, Upfile, Oldfile, Warnfile, ampbuffer)
        await ampnavigate.close()
        return

    async def hasQV(self):
        namenum = projects[elem].proj
        qvbuffer = await qvWebpage.Login(page)
        # await Debug.print('\n' + text.postloginmessage, Upfile)
        # await Debug.print('\n' + text.postloginmessage, Warnfile)
        # await Debug.print('\n' + text.postloginmessage, Oldfile)
        qvproject = await qvWebpage.gotoProject(qvbuffer, namenum)
        # await Debug.print('\nProject Switched to ' + project, Upfile)
        # await Debug.print('\nProject Switched to ' + project, Warnfile)
        # await Debug.print('\nProject Switched to ' + project, Oldfile)
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
    pass
    logging.basicConfig(level=logging.DEBUG)
    projects = await conFig.loadProjects(user)
    parallelBatches = projects.length 
    #Math.ceil(projects.length / parallel
    browser = await puppeteer.launch() #text.head
    k = 0
    for i in projects:
        # i += parallel:
        k =+ 1
        # verboselog('\nBatch ' + k + ' of ' + parallelBatches)
        promises = []
        for j in parallelBatches:
        #this doesnt work in this format, will need to rework
        #may drop parallel
            elem = i + j
            if projects[elem] != undefined and projects[elem].skip != true:
                project = projects[elem].name
                planarray = projects[elem].planarray
                usercheckpath = __dirname + '\\users\\'+ creds.user + '\\dailychecks\\' + text.filedate + '\\'
                await fs.promises.mkdir(usercheckpath, { recursive: true })
                pathtofile = usercheckpath + '_all'
                allpaths = [pathtofile+text.outputfile,pathtofile+text.pathtoOldfile,pathtofile+text.pathtoWarnfile]
                streams = await conFig.makeStream(allpaths)
                Upfile = streams[0] 
                Oldfile = streams[1] 
                Warnfile = streams[2]
                # page = await browser.newPage()
                # await Debug.print('Project:'+project+text.scanplan+planarray+'\n'+text.hasSitemessage + projects[elem].hassite + '\n', Upfile)
                # await Debug.print('Project:'+project+text.scanplan+planarray+'\n'+text.hasSitemessage + projects[elem].hassite + '\n', Warnfile)
                # await Debug.print('Project:'+project+text.scanplan+planarray+'\n'+text.hasSitemessage + projects[elem].hassite + '\n', Oldfile)
                promises.append(browser.newPage().then(
                    async page => {
                        if projects[elem].hassite == 'amp':
                            pass
                        elif projects[elem].hassite == 'qv':
                            pass
                        elif projects[elem].hassite == 'truelook': 
                            print('Truelook in develpment')
                )
                await Promise.all(promises)
    await browser.close()
    groupend('Main')
    if (verbose) {group('exitmsg')}
    console.log('\n' + text.exitmessage)
    if (verbose) {groupend('exitmsg')}
    if (preformance) {console.log(new Date().toISOString())}

    browser = await launch(headless=False)
    args: [`--window-size=${options.width},${options.height}`]
    )
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.screenshot({'path': 'example.png'})

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main(), debug=True)