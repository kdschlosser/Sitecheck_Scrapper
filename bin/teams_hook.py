"""
This sends completed cards through a webhook to a specific Team's channel (Team)
Documentation for Team's Adaptive Cards:
https://docs.microsoft.com/en-us/adaptive-cards/
"""
import json

import requests

from env import creds, text


def top_secret(channel):
    """
        Converts channel name to url from creds file
              Args:
                  channel (str): Name of channel to send card to. Currently 1 option
              Returns:
                  (str): The channel's webhook as url string
              """
    if channel == 'programming':
        print("Sending data to the Programming team")
        return creds.testhook  # programminghook
    if channel == 'flow-programming':
        print("Sending data to the Programming team through flow")
        return creds.testhook  # flow_programminghook
    elif channel == 'west_project':
        print("Sending data to West Project Checks team")
        return creds.westcoasthook  # BUILD  # return creds.westcoasthook # SHIP
    else:
        print(text.no_channel)
        return creds.testhook


async def message_factory(channel, project_name, path_to_temp):
    """
        Takes data in card format and posts it to Teams channel through a Flow webhook

        Args:
            channel(str): Selects the webhook to send too.
            project_name(str): Name of project
            path_to_temp(str): Path to file of stored json data

        Returns: Teams Hook Response code.

    """
    message = Send_Hook(channel, project_name, path_to_temp)
    return await message.draft_message()


class Send_Hook:
    """
    Send json data through a webhook to the Team's channel
    Call init as Object before calling object.draft_message() for aync factory
    """

    def __init__(self, channel, temp_project, temp_file_path):
        """
            Args:
                channel (str): Which channel(team) to send card to
                temp_project (str): Project name and filename
                temp_file_path (str): Path to json being Posted

            Returns: Teams Hook Response code.
        """
        self.channel = top_secret(channel)
        self.project = temp_project
        self.file = temp_file_path
        with open(self.file) as f:
            file = f.read()
        self.finished_card = json.loads(file)

    async def draft_message(self):
        """Prompt user to review card."""
        # TODO: build Interactive module
        # TODO: find way to display preview
        return await self.send_message()

    async def send_message(self):
        """
            Post self.finished_card to url self.channel

            Returns: Teams Hook Response code.

        """
        response = requests.post(self.channel, data=json.dumps(self.finished_card),
                                 headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            # TODO: Handle response codes
            result = ValueError(
                'Request to Teams returned an error %s, the response is:\n%s' % (response.status_code, response.text))
            return result

