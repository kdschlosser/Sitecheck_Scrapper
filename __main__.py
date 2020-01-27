#Daily Sitecheck Web Scrapper V. 4.1.0
from __future__ import print_function, unicode_literals
import sys
import io
import asyncio
import pathlib
import json
import datetime
from pyppeteer import launch
import msvcrt as m
from io import StringIO
from dateutil.relativedelta import *
from prompt_toolkit import prompt
from pyxtension.Json import Json
from PyInquirer import prompt, print_json
from env import sites, text, creds
qv = sites.qv
amp = sites.amp

#temp for build
verbose = True
getvalue = True
watchdog = 86400000
watchlimit = watchdog * 7
split = 'false'
#end temp

def wait():
    m.getch()

async def wait_type(page, selector, text):
    await page.waitForSelector(selector),
    await page.type(selector, text)
    return page

async def wait_click(page, selector):
    await page.waitForSelector(selector),
    await page.click(selector)
    return page

async def wait_hover(page, selector):
    await page.waitForSelector(selector),
    await page.hover(selector)
    return page

def loadProjects():
    with open('env/projects.json', 'r') as userdata:
        data=userdata.read()
        projects = json.loads(data)
        return projects

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
        self.project = Json(project)
        # print(self.project.planarray)
        await self.EvalSite(self)

    async def EvalSite(self):
        if self.project.skip == 'true':
            print('Skipping project: '+ self.project.name)
        else:
            print('Running project: '+ self.project.name)  #remove later
            self.streams = await conFig.makeStream(self, project_out_File(self))
            print(self.streams)
            print(text.fileheader)
            await self.filterSite(self)

    async def filterSite(self):
        if self.project.hassite == 'amp':
            await self.hasAmp(self)
        elif self.project.hassite == 'qv':
            await self.hasQV(self)

    async def hasAmp(self):
        self.url = 'https://' + self.project.name + '.geo-instruments.com/index.php'
        # # # browser = await launch({"headless": False})
        # self.page = await browser.newPage()
        # await ampWebpage.Login(self)
        await self.page.waitFor(50)
        # await ampWebpage.gotoPlanview(self)
        await self.page.waitFor(50)
        # await self.page.close()


    async def hasQV(self):
        self.url = qv.urlstring
        # browser = await launch({"headless": False})
        self.page = await browser.newPage()
        await self.page.setViewport({
            "width": 1600,
            "height": 1200})
        await qvWebpage.Login(self)
        await self.page.waitFor(50)
        await qvWebpage.gotoProject(self)
        await self.page.waitFor(50)
        await qvWebpage.gotoPlanView(self)
        await self.page.waitFor(50)
        # await self.page.close()


class ampWebpage():
    async def __init__(self):
        pass

    async def Login(self):
        await self.page.goto(self.url)
        await self.page.waitFor(500)
        await wait_type(self.page, amp.logincss, creds.username)
        await wait_type(self.page, amp.pwcss, creds.password)
        await wait_click(self,page, amp.loginbutton)
        return

    async def gotoPlanview(self):
        print(text.scanplan + self.project.planarray)
        planarray = self.project.planarray.split(",")
        for view in planarray:
            print(view)
            await self.page.goto(self.url + amp.planview + view)
            for targetchild in text.sensorarray:
                self.targetchild = targetchild
                await ampWebpage.getLastupdate(self)


    async def getLastupdate(self):
        for typeofsensorbox in amp.label:
            namesel = str('body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + self.targetchild + amp.title)
            valuesel = str('body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + self.targetchild + amp.sensor)
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
                # if getvalue:
                #     data += '\nCurrent value: ' + value

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


class qvWebpage():
    async def __init__(self):
        pass

    async def Login(self):
        await self.page.goto(self.url)
        await wait_type(self.page, qv.logincss, creds.qvuser)
        await wait_type(self.page, qv.pwcss, creds.qvpass)
        await wait_click(self.page, qv.loginbutton)
        return

    async def gotoProject(self):
        await wait_click(self.page, qv.projects)
        await wait_hover(self.page,qv.scrollbar)
        await self.page.waitFor(500)
        self.namenum = str(self.project.proj)
        print(self.namenum)
        self.page = await wait_click(self.page, qv.proj_pre + self.namenum + qv.proj_post)
        return self


    async def gotoPlanView(self):
        list = self.project.planarray.split (",")
        for view in list:
            if view != '0':
                await wait_click(self.page, qv.views)
                await self.page.waitFor(500)
                await wait_hover(self.page, qv.scrollbar2)
                await self.page.waitFor(400)
                await wait_click(self.page, qv.thumb+view)
            else:
                pass
            await self.page.waitFor(1000)
            for targetchild in text.sensorarray:
                await qvWebpage.getLastupdate(self, targetchild)

        return self


    async def getLastupdate(self, targetchild):
        sensor = '#objects > img:nth-child(' + targetchild + ')'
        try:
            await self.page.hover(sensor)
            link = await self.page.querySelector(qv.hoverbox)
            txt =  await self.page.evaluate('(link) => link.innerHTML', link)
            spltd = txt.split('<br>')
            data = '\nSensor name: ' + spltd[0]
            date = spltd[3].split("data: ").pop()
            # print(data + ' \nDate:\n' + date + '\n', Upfile)
            pdate = relitive (date)
            pnowdate = '' #Date.parse(text.nowdate)
            diff = pnowdate - pdate
            if diff <= watchdog:
                data += date
                # if verbose:
                #     data += '\n' + text.uptoDate
                print(data, Upfile)
            elif diff >= watchdog and diff <= watchlimit:
                data += date
                # if verbose:
                #     data += '\n' + text.behindDate
                print(data, Warnfile)
            else:
                data += date
                # if verbose:
                #     data += '\n' + text.oldDate

                print(data, Oldfile)
        except: #(UnhandledPromiseRejectionWarning):
            pass
        return

async def main():
    global browser
    browser = await launch({"headless": False})
    projects = loadProjects()
    [await (Controller(project)) for project in projects]
    await browser.close()

if __name__ == '__main__':
    run = asyncio.run(main())
    print('\n' + text.exitmessage)
