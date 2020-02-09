# Daily Sitecheck Web Scrapper V. 0.5.1
from __future__ import print_function, unicode_literals

import json
import os
import pathlib

import asyncio
from dateutil.parser import parse
from pyppeteer import launch
from pyxtension.Json import Json

# noinspection PyPep8Naming
from bin import Teams_card_generator as tcg, teams_hook as hook
from env import sites, text, creds

qv = sites.qv
amp = sites.amp


class Options:
    """This class contains the browser's configurable options"""
    headless = False
    # TODO: Setup .args
    chrome_args = ['--start-maximized', ' --user-data-dir=' + text.ROOT_data]
    width = text.width
    height = text.height - 200
    # TODO: update Verbose mode
    verbose = True
    getvalue = True
    watchdog = 86400
    watch_limit = watchdog * 7


def project_out_file(self) -> object:
    """
    Config project to output to the shared run file or it's own seperate file

    Returns:
        object: paths to project's output files
    """
    check_path = '\\users\\' + creds.user + '\\dailychecks\\' + text.filedate + '\\'
    pathlib.Path(check_path).mkdir(parents=True, exist_ok=True)
    if self.project.group:
        output_pre = str(check_path) + 'all_'
    else:
        output_pre = str(check_path) + str(self.project.name) + '_'
    return [output_pre + text.outputfile, output_pre + text.Oldfile, output_pre + text.Warnfile]


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
    await page.waitForSelector(selector),
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
        project: Object containing all project data:
                 group, hassite, name, playarray, proj, skip

    Returns: Todo: setup promise return hook result

    """
    run_result = Project_run(project)
    await run_result.evaluate_site()
    return run_result


async def login(self):
    """
        # TODO fill this in
    Returns:

    """
    await self.page.goto(self.url)
    await self.page.waitFor(1000)
    for x in [amp, qv]:
        try:
            await self.page.type(x.logincss, x.username)
            await self.page.type(x.pwcss, x.password)
            await self.page.click(x.loginbutton)
            break
        except:
            pass
    await self.page.waitFor(50)


class Project_run:
    """
    Controller class for a project.
    After initiation by run_controller, The Project's skip value is checked and canceled if true
    If False, the run begins.
    """

    def __init__(self, project):
        self.project = Json(project)

    async def evaluate_site(self):
        """
        after initiation by run_controller, The Project's skip value is checked and canceled if true (case sensitive).
        If false, the run begins.
        """
        if self.project.skip == 'true':
            if Options.verbose:
                print('Skipping project: ' + self.project.name)
            pass
        else:
            if Options.verbose:
                print(text.fileheader + self.project.name)
            await self.filter_site()

    async def filter_site(self):
        """
        Checks if a project has a site on Amp, Qv, or               Truelook.
        """
        # TODO: Change If to switch for multi-site projects
        if self.project.hassite == 'amp':
            await self.has_amp()
        elif self.project.hassite == 'qv':
            await self.has_QV()  # TODO rebuild truelook support

    async def has_amp(self):
        """
            Main Thread function of the Amp scanner.
            Creates the new page and gives it a viewport.
            Than handles gathering and output of data for Amp scanner.
        """
        self.url = 'https://' + self.project.name + '.geo-instruments.com/index.php'
        self.page = await browser.newPage()
        await self.page.setViewport({"width": Options.width, "height": Options.height})
        await login(self)
        await ampWebpage.goto_plan_view(self)
        await self.page.close()
        # After the Site is scanned, the collected data is processed into a
        # Team's channel card
        print(self.project.name)

        staged_file = tcg.generator(self.project)
        path_to_temp = staged_file.compile_data()
        print(path_to_temp)
        # SHIP result = await hook.message_factory(self.project.channel, self.project.name, path_to_temp)
        result = await hook.message_factory('test', self.project.name, path_to_temp)  # BUILD
        print(result, '\n End of run')

    async def has_QV(self):
        """
            Main Thread function of the QV scanner.
            Creates the new page and gives it a viewport.
            Than handles gathering and output of data for QV scanner.
        """
        # TODO Update qv run
        self.url = qv.urlstring
        self.page = await browser.newPage()
        await self.page.setViewport({"width": Options.width, "height": Options.height})
        await login(self)
        await qvWebpage.goto_project(self)
        await self.page.waitFor(50)
        await qvWebpage.goto_plan_view(self)
        await self.page.close()
        staged_file = tcg.generator(self.project)
        path_to_temp = staged_file.compile_data()
        print(path_to_temp)
        # SHIP result = await hook.message_factory(self.project.channel, self.project.name, path_to_temp)
        result = await hook.message_factory('test', self.project.name, path_to_temp)  # BUILD
        print(result, '\n End of run')


class ampWebpage:
    """
        Thread pool for Amp.
    """

    def __init__(self):
        # TODO Update class structure with my new learns
        pass

    async def goto_plan_view(self):
        """
            Navigates to each planview listed in project.planarray and iterates through an array to check possible sensorboxes
        Returns:

        """
        if Options.verbose:
            print(text.scanplan + self.project.planarray)
        plan_array = self.project.planarray.split(",")
        for view in plan_array:
            if Options.verbose:
                print(view)
            await self.page.goto(self.url + amp.planview + view)
            for target_child in range(0, 300):
                # noinspection PyAttributeOutsideInit
                self.target_child = str(target_child)
                await ampWebpage.get_last_update(self)

    async def get_last_update(self):
        """
            Collects Amp Sensor data from the current Planview

        Args:
            target_child(str): Sensor to Scan

        Returns: (none)

        """
        for type_of_sensor_box in amp.label:
            name_sel = str(
                    'body > div:nth-child(' + type_of_sensor_box + ') > div:nth-child(' + self.target_child + amp.title)
            value_sel = str(
                    'body > div:nth-child(' + type_of_sensor_box + ') > div:nth-child(' + self.target_child + amp.sensor)
            name = await self.page.J(name_sel)
            link = await self.page.J(value_sel)
            if name is None:
                pass
            else:
                # TODO When sensor is found, add to list saved to this project for future runs
                sensor = await self.page.evaluate('(name) => name.textContent', name)
                value = await self.page.evaluate('(link) => link.textContent', link)
                date = await self.page.evaluate('(link) => link.title', link)

                sensor_data = '\nSensor name: ' + sensor
                if Options.getvalue:
                    sensor_data += '\nCurrent value: ' + value
                sensor_data += '\nLatest data on AMP: '

                diff_in_days = parse(text.nowdate) - parse(date)
                diff = int(diff_in_days.total_seconds())
                sensor_data += date

                if diff <= Options.watchdog:
                    if Options.verbose:
                        sensor_data += '\n' + text.uptoDate
                    data_list = [sensor, 'good', 'Up-to-date', date]
                    tcg.store(self.project.name, data_list)
                    print(sensor_data)
                elif Options.watchdog <= diff <= Options.watch_limit:
                    if Options.verbose:
                        sensor_data += '\n' + text.behindDate
                    data_list = [sensor, 'warning', 'Older than 24 hours', date]
                    tcg.store(self.project.name, data_list)
                    print(sensor_data)
                else:
                    if Options.verbose:
                        sensor_data += '\n' + text.oldDate
                    data_list = [sensor, 'attention', 'Older than a week', date]
                    tcg.store(self.project.name, data_list)
                    print(sensor_data)


class qvWebpage:
    """
            Thread Pool for QV
    """

    async def goto_project(self):
        """
            # TODO fill this in
        Returns:

        """
        await wait_click(self.page, qv.projects)
        await wait_hover(self.page, qv.scrollbar)
        await self.page.waitFor(500)
        # print(str(self.project.proj))
        self.namenum = str(self.project.proj)
        self.page = await wait_click(self.page, qv.proj_pre + self.namenum + qv.proj_post)
        return self

    async def goto_plan_view(self) -> object:
        """
            # TODO fill this in
        Returns:
            object:
        """
        if Options.verbose:
            print(text.scanplan + self.project.planarray)
        views = self.project.planarray.split(",")
        for view in views:
            print(view)
            if view == '0':
                pass
            else:
                await wait_click(self.page, qv.views)
                await self.page.waitFor(500)
                await wait_hover(self.page, qv.scrollbar2)
                await self.page.waitFor(400)
                await wait_click(self.page, qv.thumb + view)
            await self.page.waitFor(2000)
            for target_child in range(0, 300):
                # noinspection PyAttributeOutsideInit
                self.target_child = str(target_child)
                await qvWebpage.get_last_update(self)  # return

    async def get_last_update(self):
        """
             Collects QV Sensor data from the current Planview

        Args:
            target_child(str): Sensor to Scan

        Returns: (none)

        """
        sensor = '#objects > img:nth-child(' + self.target_child + ')'
        # noinspection PyBroadException
        print(sensor)
        try:
            await self.page.hover(sensor)
            link = await self.page.J(qv.hoverbox)
            txt = await self.page.evaluate('(link) => link.innerHTML', link)
            value = 'In Development'
            split_date = txt.split('<br>')
            print(split_date)
            sensor = split_date[0]
            print(sensor, split_date[1])
            sensor_data = '\nSensor name: ' + sensor
            if Options.getvalue:
                print('In Development')
                # sensor_data += '\nCurrent value: ' + value
            date = split_date[3].split("data: ").pop()
            sensor_data += '\nLatest data on QV: '

            diff_in_days = parse(text.nowdate) - parse(date)
            diff = (diff_in_days.total_seconds())
            sensor_data += date

            if diff <= Options.watchdog:
                if Options.verbose:
                    sensor_data += '\n' + text.uptoDate
                data_list = [sensor, 'good', 'Up-to-date', date]
                tcg.store(self.project.name, data_list)
                print(sensor_data)
            elif Options.watchdog <= diff <= Options.watch_limit:
                if Options.verbose:
                    sensor_data += '\n' + text.behindDate
                data_list = [sensor, 'warning', 'Older than 24 hours', date]
                tcg.store(self.project.name, data_list)
                print(sensor_data)
            else:
                if Options.verbose:
                    sensor_data += '\n' + text.oldDate
                data_list = [sensor, 'attention', 'Older than a week', date]
                tcg.store(self.project.name, data_list)
                print(sensor_data)
        except:
            # TODO: build proper exception for not finding selector on page
            # This exception allows selector values not present on the current page to be ignored. Tag - future optimizations
            pass
        # TODO: Add check if data is empty to re-try with longer page load wait
        return


async def main():
    # noinspection PyGlobalUndefined
    global browser
    browser = await launch({"headless": Options.headless, "ignoreHTTPSErrors": True}, args=Options.chrome_args)
    projects = load_projects()
    [await (run_controller(project)) for project in projects]
    await browser.close()


if __name__ == '__main__':
    run = asyncio.run(main())
    print('\n' + text.exitmessage)
