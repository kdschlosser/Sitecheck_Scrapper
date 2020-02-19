# -*- coding: utf-8 -*-

"""
This file is part of the **pyppeteer_sitecheck_scrapper**
project git@geodev.geo-instruments.com:DanEdens/pyppet_sitecheck_scrapper.git

:platform: Windows
:license:
:synopsis: This module sends Adaptive cards to a Teams channel through a Power Automate requests Flow

    Documentation for Team's Adaptive Cards:
    https://docs.microsoft.com/en-us/adaptive-cards/

    Documentation for Power Automate: Adaptive cards in Microsoft Teams
    https://docs.microsoft.com/en-us/power-automate/create-adaptive-cards-teams

.. moduleauthor::  Dan Edens @DanEdens <Dan.Edens@geo-instruments.com>
"""

# __version__= "0.3.0"
# __author__ = "Dan Edens"
# __email__ = "Dan.Edens@Geo-Instruments.com"

import json
import requests

from ..env import creds


def top_secret(channel):
    """
    Converts channel name to Webhook url from creds file

    :param channel: Name of project's target Team's channel
    :type channel: str

    :returns: URL to channels webhook
    :rtype: str

    """
    print("Sending data to " + channel)

    if channel == 'programming':
        return creds.programminghook
    elif channel == 'west_project':
        return creds.westcoasthook
    else:
        return creds.testhook


async def message_factory(channel, project_name, path_to_temp):
    """
        Takes gathered data in card format and posts it to Teams channel through a Flow webhook
        Async factory for draft_message

            Args:
                channel(str): Selects the webhook to send too.
                project_name(str): Name of project
                path_to_temp(str): Path to file of stored json data
            Returns: (str)
                Teams Hook Response code.
    """
    message = SendHook(channel, project_name, path_to_temp)
    return await message.draft_message()


class SendHook(object):
    """
    Send json data through a webhook to the Team's channel

    Load Card.json for use in message functions.

    """
    def __init__(self, channel, temp_project, temp_file_path):
        """
        Constructor

        :param channel: Which channel(team) to send card to
        :type channel: str

        :param temp_project:Project name and filename
        :type temp_project: str

        :param temp_file_path:Path to json being Posted
        :type temp_file_path: str
        """
        self.channel = top_secret(channel)
        self.project = temp_project
        self.file = temp_file_path

        with open(self.file) as f:
            file = f.read()

        self.finished_card = json.loads(file)

    async def draft_message(self):
        """
        If the flag for review card is true:
        Prompt the user to approve the generated card before sending it to Teams.

        :returns: Teams Hook Response code.
        :rtype: str
        """
        # TODO: build Interactive module
        # TODO: find way to display preview
        return await self.send_message()

    async def send_message(self):
        """
        HTTP Post self.finished_card to self.channel

        :returns: Teams Hook Response code.
        :rtype: str
        """
        response = requests.post(
            self.channel,
            data=json.dumps(self.finished_card),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            return ValueError(
                'Request to Teams returned an error %s, the response is:\n%s' % (
                    response.status_code,
                    response.text
                )
            )

