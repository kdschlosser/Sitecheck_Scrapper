# Daily Sitecheck Web Scrapper V. 0.5.1
from __future__ import print_function, unicode_literals

import json
import msvcrt
import os
import pathlib

import asyncio
from dateutil.parser import parse
from pyppeteer import launch
from pyxtension.Json import Json

from bin import Teams_card_generator as tcg, teams_hook as hook
# noinspection PyPep8Naming
from env import sites, text, creds

qv = sites.qv
amp = sites.amp


class Options:
    """This class contains the browser's configurable options"""
    headless = True
    chrome_args = [
            '--start-maximized',
            ' --user-data-dir=' + text.ROOT_data
    ]
    width = text.width
    height = text.height - 200
    verbose = True
    getvalue = True
    watchdog = 86400
    watch_limit = watchdog * 7


def wait():
    msvcrt.getch()


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
    Wait for a selector to load than click on it.
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


def load_projects():
    """
    Returns: project object

    """
    with open('env/projects.json') as user_data:
        data = user_data.read()
        projects = json.loads(data)
    return projects


def project_out_file(self) -> object:
    """

    Returns:
        object:
    """
    check_path = '\\users\\' + creds.user + '\\dailychecks\\' + text.filedate + '\\'
    pathlib.Path(check_path).mkdir(parents=True, exist_ok=True)
    if self.project.group:
        output_pre = str(check_path) + 'all_'
    else:
        output_pre = str(check_path) + str(self.project.name) + '_'
    return [output_pre + text.outputfile, output_pre + text.Oldfile, output_pre + text.Warnfile]


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


class Project_run:
    def __init__(self, project):
        self.project = Json(project)


    async def evaluate_site(self):
        if self.project.skip == 'true':
            if Options.verbose:
                print('Skipping project: ' + self.project.name)
            pass
        else:
            print(text.fileheader + self.project.name)
            await self.filter_site()

    async def filter_site(self):
        if self.project.hassite == 'amp':
            await self.has_amp()
        elif self.project.hassite == 'qv':
            await self.has_QV()
        # TODO rebuild truelook support

    async def has_amp(self):
        self.url = 'https://' + self.project.name + '.geo-instruments.com/index.php'
        self.page = await browser.newPage()
        await self.page.setViewport({
                "width":  Options.width,
                "height": Options.height})
        await ampWebpage.login(self)
        await self.page.waitFor(50)
        await ampWebpage.goto_plan_view(self)
        await self.page.close()
        # After the Site is scanned, the collected data is processed into a
        # Team's channel card
        print(self.project.name)

        staged_file = tcg.generator(self.project)
        path_to_temp = staged_file.compile_data()
        print(path_to_temp)
        # Now that the data is arranged, pass it on to teams through a webhook
        # result = await hook.message_factory(self.project.channel, self.project.name, path_to_temp)
        result = await hook.message_factory('test', self.project.name, path_to_temp)
        print(result, '\n End of run')

    async def has_QV(self):
        #TODO Update qv run
        self.url = qv.urlstring
        self.page = await browser.newPage()
        await self.page.setViewport({
                "width":  Options.width,
                "height": Options.height})
        await qvWebpage.login(self)
        await self.page.waitFor(50)
        await qvWebpage.goto_project(self)
        await self.page.waitFor(50)
        await qvWebpage.goto_plan_view(self)
        await self.page.close()


class ampWebpage:
    def __init__(self):
        # TODO Update class structure with my new learns
        pass

    async def login(self):
        await self.page.goto(self.url)
        await self.page.waitFor(1000)
        await wait_type(self.page, amp.logincss, creds.username)
        await wait_type(self.page, amp.pwcss, creds.password)
        await wait_click(self.page, amp.loginbutton)
        # TODO move to cleanup function, add name_temp.json
        if os.path.exists(tcg.storage + self.project.name + '_temp.txt'):
            os.remove(tcg.storage + self.project.name + '_temp.txt')
        return

    async def goto_plan_view(self):
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
        return self

    async def get_last_update(self):
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
                print(sensor, value)
                data = '\nSensor name: ' + sensor
                if Options.getvalue:
                    # TODO Add get value option to card generator
                    data += '\nCurrent value: ' + value
                data += '\nLast Updated on AMP: '
                diff_in_days = parse(text.nowdate) - parse(date)
                diff = int(diff_in_days.total_seconds())
                if diff <= Options.watchdog:
                    data += date
                    if Options.verbose:
                        data += '\n' + text.uptoDate
                    print(data)
                    # data = [name, color, status, time]
                    data_list = [sensor, 'good', 'Up-to-date', date]
                    tcg.store(self.project.name, data_list)
                elif Options.watchdog <= diff <= Options.watch_limit:
                    data += date
                    if Options.verbose:
                        data += '\n' + text.behindDate
                    if Options.check:
                        # TODO: Build check module, Entry point here
                        pass
                    print(data)
                    data_list = [sensor, 'warning', 'Older than 24 hours', date]
                    tcg.store(self.project.name, data_list)
                else:
                    data += date
                    if Options.verbose:
                        data += '\n' + text.oldDate
                    print(data)
                    data_list = [sensor, 'attention', 'Older than a week', date]
                    tcg.store(self.project.name, data_list)


class qvWebpage:
    def __init__(self):
        # TODO Update qv run
        pass

    async def login(self):
        await self.page.goto(self.url)
        await wait_type(self.page, qv.logincss, creds.qvuser)
        await wait_type(self.page, qv.pwcss, creds.qvpass)
        await wait_click(self.page, qv.loginbutton)
        return

    async def goto_project(self):
        await wait_click(self.page, qv.projects)
        await wait_hover(self.page, qv.scrollbar)
        await self.page.waitFor(500)
        # print(str(self.project.proj))
        self.namenum = str(self.project.proj)
        self.page = await wait_click(self.page, qv.proj_pre + self.namenum + qv.proj_post)
        return self

    async def goto_plan_view(self) -> object:
        """

        Returns:
            object:
        """
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
                await qvWebpage.get_last_update(self, target_child)
        # return

    async def get_last_update(self, target_child):
        sensor = '#objects > img:nth-child(' + str(target_child) + ')'
        # noinspection PyBroadException
        try:
            await self.page.hover(sensor)
            link = await self.page.querySelector(qv.hoverbox)
            txt = await self.page.evaluate('(link) => link.innerHTML', link)
            split_date = txt.split('<br>')
            sensor_data = '\nSensor name: ' + split_date[0]
            date = split_date[3].split("data: ").pop()
            sensor_data = sensor_data + ' \nDate:' + date + '\n'
            diff_in_days = parse(text.nowdate) - parse(date)
            diff = (diff_in_days.total_seconds())
            if diff <= Options.watchdog:
                sensor_data += date
                if Options.verbose:
                    sensor_data += '\n' + text.uptoDate
                print(sensor_data)
            elif Options.watchdog <= diff <= Options.watch_limit:
                sensor_data += date
                if Options.verbose:
                    sensor_data += '\n' + text.behindDate
                print(sensor_data)
            else:
                sensor_data += date
                if Options.verbose:
                    sensor_data += '\n' + text.oldDate
                print(sensor_data)
        # This exception allows selector values not present on the current page to be ignored. Tag - future optimizations
        except:
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
