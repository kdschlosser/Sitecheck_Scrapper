"""
    This module sends Adaptive cards to a Teams channel through a Power Automate requests Flow

    Documentation for Team's Adaptive Cards:
    https://docs.microsoft.com/en-us/adaptive-cards/

    Documentation for Power Automate: Adaptive cards in Microsoft Teams
    https://docs.microsoft.com/en-us/power-automate/create-adaptive-cards-teams
"""
# __version__= "0.2.0"
# __author__ = "Dan Edens"
# __email__ = "Dan.Edens@Geo-Instruments.com"
# __status__ = "Production"

import json

import requests

from env import creds, text


def top_secret(channel):
    """
        Converts channel name to Webhook url from creds file
        These Urls need to be kept internal. RISK: LOW
        Chance of a compromised link being spammed is very low, but possible.

            Args:
                channel (str): Name of project's target Team's channel
            Returns:
                webhook(str): URL to channels webhook
    """
    if channel == 'programming':
        print("Sending data to the Programming team")
        return creds.testhook  # SHIP programminghook
    if channel == 'flow-programming':
        print("Sending data to the Programming team through flow")
        return creds.testhook  # SHIP flow_programminghook
    elif channel == 'west_project':
        print("Sending data to West Project Checks team")
        return creds.testhook  # SHIP creds.westcoasthook
    else:
        print(text.no_channel)
        return creds.testhook


async def message_factory(channel, project_name, path_to_temp):
    """
        Takes gathered data in card format and posts it to Teams channel through a Flow webhook
        This function acts as an Async factory for draft_message

            Args:
                channel(str): Selects the webhook to send too.
                project_name(str): Name of project
                path_to_temp(str): Path to file of stored json data
            Returns: (str)
                Teams Hook Response code.
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
           Load Card.json for use in message functions.

               Args:
                   channel (str): Which channel(team) to send card to
                   temp_project (str): Project name and filename
                   temp_file_path (str): Path to json being Posted
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

                Args:
                    self (obj): Passes entire self through for now. TODO: trim unneeded values
                Returns: (str)
                    Teams Hook Response code.
        """
        # TODO: build Interactive module
        # TODO: find way to display preview
        return await self.send_message()

    async def send_message(self):
        """
            HTTP Post self.finished_card to self.channel

                Args:
                    Self.finished_card (str): Path to Card.json
                    self.channel (str): Webhook Url to target channel
                Returns: (str)
                    Teams Hook Response code.
        """
        response = requests.post(self.channel, data=json.dumps(self.finished_card),
                                 headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            return ValueError('Request to Teams returned an error %s, the response is:\n%s' % (
            response.status_code, response.text))


if __name__ == "__main__":
