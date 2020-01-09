#Daily Sitecheck Web Scrapper V. 4.0.0
import sys
import asyncio
import json
from pyppeteer import launch
from env import sites,text,creds

defaultfile = 'notes.txt'

# parse file
# print(obj[2])
class Debug:
    def log(data, file)
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
        
class Config:
    def _init_ (self):
        pass

    def loadProjects (user): 
        #let proj = __dirname + '/users/'+user+'/projects.json'
        with open('env/projects.json', 'r') as userdata:
            data=userdata.read()
            projectlist = json.loads(data)
            return projectlist

    def makeStream(path):
        #check path exists
        for x in path:
            print(x)
            streams += x
        return streams

class Report:
    def genCsv(data):
        pass




projects = Config.loadProjects('dan.edens')
print(projects)



# async def main():
    
    # browser = await launch(headless=False)
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