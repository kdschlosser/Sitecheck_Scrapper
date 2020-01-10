#Daily Sitecheck Web Scrapper V. 4.0.0
import sys
import asyncio
import json
from pyppeteer import launch
from env import sites, text, creds

#temp for build
debug = 0
self = ''
#end temp


# print(obj[2])
class Debug():
    def __init__(self, data, wfile):
        self.data = data
        if not wfile:
            wfile = 'notes.txt'
        else:
            pass
        self.wfile = wfile
        
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
        #let proj = __dirname + '/users/'+user+'/projects.json'
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
            await Debug.print(text.loginmessage + view + '\n', self.Upfile)
            await Debug.print(text.loginmessage + view + '\n', self.Warnfile)
            await Debug.print(text.loginmessage + view + '\n', self.Oldfile)
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


#     async def getLastupdate(self, targetchild):
#         let sensor = '#objects > img:nth-child(' + targetchild + ')';
#         try:
#             await self.page.hover(sensor);
#             group('Sensor: ' + sensor);
#             const link = await self.page.$(sites.qv.hoverbox);
#             const txt =  await self.page.evaluate(link => link.innerHTML, link);
#             let spltd = txt.split('<br>');
#             let data = '\nSensor name: ' + spltd[0];
#             let date = spltd[3].split("data: ").pop();
#             // await Debug.print(data + ' \nDate:\n' + date + '\n', Upfile);
#             const pdate = Date.parse(date);
#             const pnowdate = Date.parse(text.nowdate);
#             const diff = Math.abs(pnowdate - pdate);
#             if (diff < watchdog ) {
#                 data += date;
#                 if (verbose) {data += '\n' + text.uptoDate};
#                 await Debug.print(data, Upfile);
#             } else if (diff > watchdog & diff < watchlimit) {
#                 data += date;
#                 if (verbose) {data += '\n' + text.behindDate};
#                 await Debug.print(data, Warnfile);
#             } else {
#                 data += date;
#                 if (verbose) {data += '\n' + text.oldDate};
#                 await Debug.print(data, Oldfile);
#             };
#             groupend('Sensor: ' + targetchild);
#         }
#         except(UnhandledPromiseRejectionWarning) {};
#         return;
#     };
# };

# async def main():
    
    # browser = await launch(headless=False
    # args: [`--window-size=${options.width},${options.height}`]
    # )
    # page = await browser.newPage()
#     await page.goto('http://example.com')
#     await page.screenshot({'path': 'example.png'})

#     dimensions = await page.evaluate('''() => {
#         return {
#             width: document.documentElement.clientWidth,
#             height: document.documentElement.clientHeight,
#             deviceScaleFactor: window.devicePixelRatio,
#         }
#     }''')

#     print(dimensions)
#     # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
#     await browser.close()

# asyncio.get_event_loop().run_until_complete(main())