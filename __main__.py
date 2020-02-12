"""
    Geo-Instruments
    Daily Sitecheck Scanner
    Repository: https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper
"""
# __author__ = "Dan Edens"
# __version__= "0.5.3"

from __future__ import print_function, unicode_literals

import json
import os

import asyncio
from dateutil.parser import parse
from pyppeteer import launch
from pyppeteer.errors import PageError
from pyxtension.Json import Json

# noinspection PyPep8Naming
from bin import teams_card_generator as tcg, teams_hook as hook
from env import sites, text

qv = sites.qv
amp = sites.amp


class Options:
    """This class contains the browser's configurable options"""
    headless = False
    # TODO: Setup .args
    chrome_args = ['--start-maximized', ' --user-data-dir='+text.ROOT_data]
    width = text.width
    height = text.height-200
    verbose = True
    getvalue = True
    watchdog = 86400
    watch_limit = watchdog * 7


def verbose(verbose_text):
    """
        Verbose Mode print function

        Args:
            verbose_text(str): Text to print
    """
    if Options.verbose:
        print(verbose_text)


def load_projects():
    """
        Returns: project object
    """
    with open('env/projects.json') as user_data:
        data = user_data.read()
        projects = json.loads(data)
    return projects


async def wait_type(page, selector, txt):
    """
        Wait for a selector to load than type supplied text.
        Returns page in case entering text changes the context.
    """
    await page.waitForSelector(selector)
    await page.type(selector, txt)
    return page


async def wait_click(page, selector):
    """
        Wait for a selector to load than clicks on it.
        Returns page in case this changes the context.
    """
    await page.waitForSelector(selector),
    await page.click(selector)
    return page


async def wait_hover(page, selector):
    """
        Wait for a selector to load than hover over it.
        Returns page in case this changes the context.
    """
    await page.waitForSelector(selector),
    await page.hover(selector)
    return page


async def run_controller(project):
    """
        Args:
            project: Object containing project data:
                     group, hassite, name, playarray, proj, skip
        Returns:
            Todo: setup promise return hook result
    """
    run_result = Project_run(project)
    await run_result.skip_site()
    return run_result


async def watchdog_processor(diff, sensor_data, project_name, sensor, date):
    """
        Handles sorting sensor watchdog status.
            Up-to-date, Behind, Old

        Args:
            diff (int): Time since last reading
            sensor_data (str): Text block that is rinted to console
            project_name(str): Name of Project
            sensor (str): Sensor ID
            date (str): Formatted Date string
    """
    if diff <= Options.watchdog:
        if Options.verbose:
            sensor_data += '\n'+text.uptoDate
            print(sensor_data)
        data_list = [sensor, 'good', 'Up-to-date', date]
        tcg.store(project_name, data_list)
    elif Options.watchdog <= diff <= Options.watch_limit:
        if Options.verbose:
            sensor_data += '\n'+text.behindDate
            print(sensor_data)
        data_list = [sensor, 'warning', 'Older than 24 hours', date]
        tcg.store(project_name, data_list)
    else:
        if Options.verbose:
            sensor_data += '\n'+text.oldDate
            print(sensor_data)
        data_list = [sensor, 'attention', 'Older than a week', date]
        tcg.store(project_name, data_list)


async def login(self):
    """
        Handles Url Navigation and Login Authentication.

        Returns:
            (none)

    """
    await self.page.goto(self.url)
    await self.page.waitFor(1000)
    for x in [amp, qv]:
        try:
            await self.page.type(x.logincss, x.username)
            await self.page.type(x.pwcss, x.password)
            await self.page.click(x.loginbutton)
            verbose(text.loginmessage)
            break
        except PageError:
            pass
    await self.page.waitFor(50)


async def scan_plan_view(parent, thread_pool):
    """
        Iterate through Array of possible Sensor selectors on current planview.
            Absolute selector:
            'body > div:nth-child('(3:4)') > div:nth-child('(0:300)') > a:nth-child(1)'
            Relative selector:
            'body >' + amp.csspath + type_of_sensor_box + ') ' + amp.csspath + self.target_child + amp.title
        Args:
            parent: <__main__.Project_run object at ** >
            thread_pool: <class '__main__.Amp_Webpage'>
    """
    print(parent)
    for target_child in range(0, 300):
        parent.target_child = str(target_child)
        await thread_pool.get_last_update(parent)


class Project_run:
    """
        Controller class for project

        Json is ``dict`` subclass to represent a Json object
        For more information see [Pytenshion](https://pypi.org/project/pyxtension/)
        This gives the
    """

    def __init__(self, project):
        self.project = Json(project)

    async def skip_site(self):
        """
            Cancels run if project.skip is true
        """
        if self.project.skip == 'true':
            verbose('Skipping project: '+self.project.name)
            pass
        else:
            verbose(text.fileheader+self.project.name)
            await self.filter_site()

    async def filter_site(self):
        """
            Checks if a project is housed on Amp, Qv, and/or Truelook.
        """
        # TODO Convert this to unique filename for each run
        if os.path.exists(tcg.storage+self.project.name+'_temp.txt'):
            os.remove(tcg.storage+self.project.name+'_temp.txt')
        if os.path.exists(tcg.storage+self.project.name+'_temp.json'):
            os.remove(tcg.storage+self.project.name+'_temp.json')
        # TODO: Change If to switch for multi-site projects
        if self.project.hassite == 'amp':
            await self.has_amp()
        elif self.project.hassite == 'qv':
            await self.has_QV()  # TODO rebuild truelook support
        elif self.project.hassite == 'truelook':
            verbose('In Development')

    async def has_amp(self):
        """
            Main Thread of the Amp scanner.
            Creates the new page and gives it a viewport.
            Than handles gathering and output of data for Amp scanner.
        """
        self.url = 'https://'+self.project.name+'.geo-instruments.com/index.php'
        self.page = await browser.newPage()
        await self.page.setViewport({"width": Options.width, "height": Options.height})
        await login(self)
        await Amp_Webpage.goto_plan_view(self)
        await self.page.close()
        verbose(self.project.name)
        staged_file = tcg.Generator(self.project)
        path_to_temp = staged_file.compile_data()
        verbose(path_to_temp)
        result = await hook.message_factory(self.project.channel, self.project.name, path_to_temp)
        verbose(result, '\n End of run')

    async def has_QV(self):
        """
            Main Thread of the QV scanner.
            Creates the new page and gives it a viewport.
            Than handles gathering and output of data for QV scanner.
        """
        self.url = qv.urlstring
        self.page = await browser.newPage()
        await self.page.setViewport({"width": Options.width, "height": Options.height})
        await login(self)
        await Qv_Webpage.goto_project(self)
        await self.page.waitFor(50)
        await Qv_Webpage.goto_plan_view(self)
        await self.page.close()
        staged_file = tcg.Generator(self.project)
        path_to_temp = staged_file.compile_data()
        verbose(path_to_temp)
        result = await hook.message_factory(self.project.channel, self.project.name, path_to_temp)
        verbose(result, '\n End of run')


class Amp_Webpage:
    """
        Thread pool for Amp.
    """

    async def goto_plan_view(self) -> object:
        """
            Navigates to each planview listed in project.planarray and
            iterates through an array to check over sensor boxes

            Args:
                self.project.planarray(list):

            Returns:
                (none)
        """
        verbose(text.scanplan+self.project.planarray)
        plan_array = self.project.planarray.split(",")
        for view in plan_array:
            verbose(view)
            await self.page.goto(self.url+amp.planview+view)
            await scan_plan_view(self, Amp_Webpage)

    async def get_last_update(self):
        """
            Collects Sensor data for the provided sensor ID (self.target_child)

            Args: TODO trim methods
                self.page(obj): Page Context
                self.project.name(str): Project name
                self.target_child(str): Sensor to Scan
            Returns:
                (none)
        """
        for type_of_sensor_box in amp.label:
            name_sel = str('body '+amp.csspath+type_of_sensor_box+')'+amp.csspath+self.target_child+amp.title)
            value_sel = str('body '+amp.csspath+type_of_sensor_box+')'+amp.csspath+self.target_child+amp.sensor)
            name = await self.page.J(name_sel)
            link = await self.page.J(value_sel)
            if name is None:
                pass
            else:
                sensor = await self.page.evaluate('(name) => name.textContent', name)
                value = await self.page.evaluate('(link) => link.textContent', link)
                date = await self.page.evaluate('(link) => link.title', link)
                sensor_data = '\nSensor name: '+sensor
                if Options.getvalue:
                    sensor_data += '\nCurrent value: '+value
                sensor_data += '\nLatest data on AMP: '
                diff_in_days = parse(text.nowdate)-parse(date)
                diff = int(diff_in_days.total_seconds())
                sensor_data += date
                await watchdog_processor(diff, sensor_data, self.project.name, sensor, date)


class Qv_Webpage:
    """
        Thread Pool for QV
    """

    async def goto_project(self):
        """
            Navigates to project as defined by project.proj and
            iterates through project views
                Returns:
                    (none)
        """
        await wait_click(self.page, qv.projects)
        await wait_hover(self.page, qv.scrollbar)
        await self.page.waitFor(500)
        self.namenum = str(self.project.proj)
        self.page = await wait_click(self.page, qv.proj_pre+self.namenum+qv.proj_post)


    async def goto_plan_view(self) -> object:
        """
            Navigates to each planview listed in project.planarray and
            iterates through hoving on each sensor, gathering data from the
            loaded Hoverbox
                Returns:
                    (none)
        """
        verbose(text.scanplan+self.project.planarray)
        views = self.project.planarray.split(",")
        for view in views:
            print(view)
            if view == '0':
                pass
            else:
                await wait_click(self.page, qv.views)
                await self.page.waitFor(500)
                await wait_hover(self.page, qv.scrollbar2)
                await self.page.waitFor(300)
                await wait_click(self.page, qv.thumb+view)
            await self.page.waitFor(2000)
            await scan_plan_view(self, Qv_Webpage)

    async def get_last_update(self):
        """
             Collects Sensor data for the provided sensor ID (self.target_child)

                Args:
                    self.page(obj): Page Context
                    self.project.name(str): Project name
                    self.target_child(str): Sensor to Scan

                Exception handles:
                    Passes over non-existent sensors during view scan.
                    raise PageError('No node found for selector: ' + selector)
                    pyppeteer.errors.PageError: No node found for selector: #objects > img:nth-child(0)

                Returns:
                    (none)
        """
        sensor = '#objects > img:nth-child('+self.target_child+')'
        # noinspection PyBroadException
        try:
            await self.page.hover(sensor)
            link = await self.page.J(qv.hoverbox)
            txt = await self.page.evaluate('(link) => link.innerHTML', link)
            value = 'In Development'
            split_date = txt.split('<br>')
            sensor = split_date[0]
            sensor_data = '\nSensor name: '+sensor
            # if Options.getvalue: Sensor_Data += '\nCurrent value: ' + value
            date = split_date[3].split("data: ").pop()
            sensor_data += '\nLatest data on QV: '
            diff_in_days = parse(text.nowdate)-parse(date)
            diff = (diff_in_days.total_seconds())
            sensor_data += date
            await watchdog_processor(diff, sensor_data, self.project.name, sensor, date)
        except PageError:
            pass


async def main():
    """
        Application Main Thread
        Retrieves Project information from projects.json
        Loops through each and sends a card to it's Site-check channel
    """
    # noinspection PyGlobalUndefined
    global browser
    browser = await launch({"headless": Options.headless, "ignoreHTTPSErrors": True}, args=Options.chrome_args)
    projects = load_projects()
    [await (run_controller(project)) for project in projects]
    await browser.close()


asyncio.run(main())
print('\n'+text.exit_message)
