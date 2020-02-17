"""
    Geo-Instruments
    Daily Sitecheck Scanner
    Repository: https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper
"""
# __author__ = "Dan Edens"
# __version__= "0.5.6"

from __future__ import print_function, unicode_literals

import json
import os
import argparse

import asyncio
from dateutil.parser import parse
from pyppeteer import launch
from pyppeteer.errors import PageError, ElementHandleError
from pyxtension.Json import Json

from bin import teams_card_generator, teams_hook, ultis
from env import sites, text

# Readablity abbrivations
qv = sites.qv
amp = sites.amp
tcg = teams_card_generator


class Options:
    """
        Command Line argument Parser
    """
    t = text.arg_text
    parser = argparse.ArgumentParser(prog='Sitecheck Scanner', description=t.main)
    parser.add_argument('--eval', '-e', action='store_true', default=False, help=t.eval)
    parser.add_argument('--debug', '-d', action='store_true', default=False, help=t.debug)
    parser.add_argument('--verbose', '-v', action='store_true', default=False, help=t.verbose)
    parser.add_argument('--value', default=False, help=t.value)
    parser.add_argument('--headless', action='store_false', default=True, help=t.visual)
    parser.add_argument('--time', '-t', default='24', type=int, help=t.watchdog)
    parser.add_argument('--weather', '-w', action='store_true', help=t.weather)
    parser.add_argument('--project', '-p', action='append', default='All', help=t.project)
    parser.add_argument('--add-project', help=t.add_project)
    parser.add_argument('--edit-project', help=t.edit_project)
    args = parser.parse_args()
    project = args.project
    Debug = args.debug
    Verbose = args.verbose
    headless = args.headless
    watchdog = int(args.time * 3600)
    watch_limit = watchdog * 7
    chrome_args = ['--start-maximized', ' --user-data-dir='+text.ROOT_data]
    getvalue = args.value


def verbose(verbose_text):
    """
        Verbose Mode print function
            Args:
                verbose_text(str): Text to print
    """
    if Options.Verbose:
        print(verbose_text)


def debug(debug_text):
    """
        Debug Mode print function
            Args:
                debug_text(str): Text to print
    """
    if Options.Debug:
        print(debug_text)


def load_projects():
    """
        Returns (obj): project
    """
    with open('env/projects.json') as user_data:
        data = user_data.read()
        projects = json.loads(data)
    return projects


async def run_controller(project):
    """
        Args:
            project: Object containing project data:
                     group, hassite, name, playarray, proj, skip
        Returns:
            Todo: setup promise return hook result
    """
    run_result = Project_run(project)
    debug(run_result.channel)
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
        # tcg.store(project_name, data_list)
        print(sensor_data)
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
        # tcg.store(project_name, data_list)
        print(sensor_data)


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


async def scan_plan_view(parent, operator):
    """
        Iterate through Array of possible Sensor selectors on current planview.
            Absolute selector:
            'body > div:nth-child('(3:4)') > div:nth-child('(0:300)') > a:nth-child(1)'
            Relative selector:
            'body >' + amp.csspath + type_of_sensor_box + ') ' + amp.csspath + self.target_child + amp.title
        Args:
            parent: <__main__.Project_run object at ** >
            operator: <class '__main__.Amp_Webpage'>
    """
    print(parent)
    for target_child in range(0, 300):
        parent.target_child = str(target_child)
        await operator.get_last_update(parent)


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
            if Options.project != 'All' & self.project.name != Options.project:
                pass
            else:
                verbose(text.fileheader+self.project.name)
                await self.filter_site()

    async def filter_site(self):
        """
            Checks if a project is housed on Amp, Qv, and/or Truelook.
        """
        # TODO Convert this to unique filename for each run
        if os.path.exists(text.ROOT_card+self.project.name+'_temp.txt'):
            os.remove(text.ROOT_card+self.project.name+'_temp.txt')
        if os.path.exists(text.ROOT_card+self.project.name+'_temp.json'):
            os.remove(text.ROOT_card+self.project.name+'_temp.json')
        # TODO: Change If to switch for multi-site projects
        if self.project.hassite == 'amp':
            await self.has_amp()
        elif self.project.hassite == 'qv':
            await self.has_QV()  # TODO rebuild truelook support
        elif self.project.hassite == 'truelook':
            verbose('In Development')

    async def has_amp(self):
        """
            Main Operator of the Amp scanner.
            Creates the new page and gives it a viewport.
            Than handles gathering and output of data for Amp scanner.
        """
        self.url = 'https://'+self.project.name+'.geo-instruments.com/index.php'
        self.page = await browser.newPage()
        await self.page.setViewport({"width": Options.width, "height": Options.height})
        await login(self)
        await Amp_Webpage.goto_plan_view(self)
        # await self.page.close()
        await self.page.close()
        verbose(self.project.name)
        staged_file = tcg.Generator(self.project)
        path_to_temp = staged_file.compile_data()
        verbose(path_to_temp)
        result = await teams_hook.message_factory(self.project.channel, self.project.name, path_to_temp)
        verbose(result+'\n End of run')

    async def has_QV(self):
        """
            Main Operator of the QV scanner.
            Creates the new page and gives it a viewport.
            Than handles gathering and output of data for QV scanner.
        """
        self.url = qv.urlstring
        pages = await browser.pages()
        self.page = pages[0]
        await self.page.setViewport({"width": text.width, "height": text.height-200})
        await login(self)
        await Qv_Webpage.goto_project(self)
        await self.page.waitFor(50)
        await Qv_Webpage.goto_plan_view(self)
        await self.page.close()
        staged_file = tcg.Generator(self.project)
        path_to_temp = staged_file.compile_data()
        verbose(path_to_temp)
        result = await teams_hook.message_factory(self.project.channel, self.project.name, path_to_temp)
        verbose(result, '\n End of run')


class Amp_Webpage:
    """
        Operator pool for Amp.
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
        Operator pool for QV
    """

    async def goto_project(self):
        """
            Navigates to project as defined by project.proj and
            iterates through project views
                Returns:
                    (none)
        """
        await ultis.wait_click(self.page, qv.projects)
        await ultis.wait_hover(self.page, qv.scrollbar)
        await self.page.waitFor(500)
        self.namenum = str(self.project.proj)
        self.page = await ultis.wait_click(self.page, qv.proj_pre+self.namenum+qv.proj_post)

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
                await ultis.wait_click(self.page, qv.views)
                await self.page.waitFor(500)
                await ultis.wait_hover(self.page, qv.scrollbar2)
                await self.page.waitFor(300)
                await ultis.wait_click(self.page, qv.thumb+view)
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
        except (ElementHandleError, PageError, IndexError):
            pass


async def main():
    """
        Application Main Operator
        Retrieves Project information from projects.json
        Loops through each and sends a card to it's Site-check channel
    """
    # noinspection PyGlobalUndefined
    global browser
    browser = await launch({"headless": Options.headless, "ignoreHTTPSErrors": True}, args=Options.chrome_args)
    projects = load_projects()
    [await (run_controller(project)) for project in projects]
    await browser.close()


# Options = arguments.process_args()
ultis.disable_timeout_pyppeteer()
asyncio.run(main())
print('\n'+text.exit_message)
