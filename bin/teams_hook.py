"""
This sends completed cards through a webhook to a specific Team's channel (Team)
Documentation for Team's card incoming Webhooks:
https://docs.microsoft.com/en-us/micrsoftteams/platform/webhooks-and-connectors/what-are-webhooks-and-connectors

"""

import json

import requests

from env import creds


def top_secret(channel):
    """
              Args:
                  channel (str): Name of channel to send card to. Currently 1 option
              Returns:
                  (str): The channel's webhook as url string
              """
    # currently only 1 channel is setup. This will be added in future versions need
    # TODO: Build sorter to retrieve hook urls contained in creds file
    if channel == 'test':
        return 'https://webhook.site/854c483a-1a38-4523-b25e-0bb46012a101'
    elif channel == 'westproject':
        return creds.webhook_url.westproject
    elif channel == 'another_area':
        return creds.webhook_url.another_area
    else:
        # print('Channel name does not match configured projects')
        return creds.teamshook


class Send_Hook:
    def __init__(self, channel, project, file_path):
        """
                  Args:
                      channel (str): Which team to send card to. Currently 1 option
                      file_path (str): 'Path to json being Posted'
                  Returns:
                      (str): Post error message
                  """
        # converts channel name to url from creds file
        self.channel = top_secret ( channel )
        self.project = project
        self.file = file_path
        self.finished_card = json.loads ( self.file + '_card.json' )

    def draft_message(self):
        # prompt user to review card.
        # TODO: build Interactive module
        # TODO: find way to display preview
        return self.send_message ()

    def send_message(self):
        # Post self.finished_card to url self.channel
        response = requests.post (
            self.channel, data=json.dumps ( self.finished_card ),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            # return error.message. TODO: return to be handled
            raise ValueError (
                'Request to Teams returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
