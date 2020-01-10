#Daily Sitecheck Web Scrapper V. 4.0.0
import sys
import asyncio
import json
from pyppeteer import launch
from env import sites, text, creds

#temp for build
debug = 0
defaultfile = 'notes.txt'

#end temp


# print(obj[2])
class Debug:
    def log(self, data, file):
        if not file:
            file = defaultfile
        else:
            pass
        if debug == 0:
            pass
        elif debug == 1:
            pass
        elif debug == 2:
            pass
        elif debug == 3:
            pass
        return

    def askQuestion(query):    
        readline.createInterface
        input = process.stdin
        output = process.stdout
        return
    
    def checkExists(file):
        pass
        
class Config:
    def _init_ (self):
        pass

    def loadProjects (self, user): 
        #let proj = __dirname + '/users/'+user+'/projects.json'
        with open('env/projects.json', 'r') as userdata:
            data=userdata.read()
            projectlist = json.loads(data)
            return projectlist

    def makeStream(self, path):
        #check path exists
        for x in path:
            print(x)
            streams += x
        return streams

class Report:
    def genCsv(self, data):
        pass

class Ampadmin:
    async def login(self, url, page):
        await page.goto(url)
        await page.type(sites.selectors.amp.logincss, creds.credentials.username)
        await page.type(sites.selectors.amp.pwcss, creds.credentials.password)
        await page.click(sites.selectors.amp.loginbutton)
        # await page.setViewport(width(1600) height(900))
        await page.waitFor(50)
        return page
  
  
projects = Config.loadProjects('dan.edens')
print(projects)

class qvWebpage:
    async def Login(self, page):
        try:
            await page.goto(sites.qv.urlstring)
        except ERR_ADDRESS_UNREACHABLE:
            print('url error')
        await page.type(sites.qv.logincss, creds.credentials.qvuser)
        await page.type(sites.qv.pwcss, creds.credentials.qvpass)
        await page.click(sites.qv.loginbutton)
        # await page.setViewport(width: 1600, height: 900)
        await page.waitFor(2000)
        return page

#     static async gotoProject(page, namenum) {
#         group('Project');
#         await page.click(sites.qv.menuprojects);
#         await page.waitFor(200);
#         await page.hover(sites.qv.scrollbar);
#         await page.waitFor(500);
#         await page.click(sites.qv.Qvprojectpre + namenum + sites.qv.Qvprojectpost);
#         await page.waitFor(500);
#         groupend('Project');
#         return page;
#     };


#     static async gotoView(planarray, Upfile, Warnfile, Oldfile, page) {
#         for (let view of planarray) {
#             group('Planview ' + view);
#             await Debug.print(TEXT.loginmessage + view + '\n', Upfile);
#             await Debug.print(TEXT.loginmessage + view + '\n', Warnfile);
#             await Debug.print(TEXT.loginmessage + view + '\n', Oldfile);
#             if (view != '0') {
#                 await page.click(sites.qv.views);
#                 await page.waitFor(500);
#                 await page.hover(sites.qv.scrollbar2);
#                 await page.waitFor(200);
#                 await page.click(sites.qv.thumb+view);
#             } else {};
#             await page.waitFor(1000);
#             for (let targetchild of TEXT.sensorarray) {
#                 await qvWebpage.getLastupdate(targetchild, Upfile, Warnfile, Oldfile, page)};
#             groupend('Planview' + view);
#         };
#         return page;
#     };

#     static async getLastupdate(targetchild, Upfile, Warnfile, Oldfile, page) {
#         let sensor = '#objects > img:nth-child(' + targetchild + ')';
#         try {
#             await page.hover(sensor);
#             group('Sensor: ' + sensor);
#             const link = await page.$(sites.qv.hoverbox);
#             const txt =  await page.evaluate(link => link.innerHTML, link);
#             let spltd = txt.split('<br>');
#             let data = '\nSensor name: ' + spltd[0];
#             let date = spltd[3].split("data: ").pop();
#             // await Debug.print(data + ' \nDate:\n' + date + '\n', Upfile);
#             const pdate = Date.parse(date);
#             const pnowdate = Date.parse(TEXT.nowdate);
#             const diff = Math.abs(pnowdate - pdate);
#             if (diff < watchdog ) {
#                 data += date;
#                 if (verbose) {data += '\n' + TEXT.uptoDate};
#                 await Debug.print(data, Upfile);
#             } else if (diff > watchdog & diff < watchlimit) {
#                 data += date;
#                 if (verbose) {data += '\n' + TEXT.behindDate};
#                 await Debug.print(data, Warnfile);
#             } else {
#                 data += date;
#                 if (verbose) {data += '\n' + TEXT.oldDate};
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