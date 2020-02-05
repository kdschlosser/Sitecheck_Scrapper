"""
This sends completed cards through a webhook to a specific Team's channel (Team)
Documentation for Team's card incoming Webhooks:
https://docs.microsoft.com/en-us/micrsoftteams/platform/webhooks-and-connectors/what-are-webhooks-and-connectors

"""

import json

import requests

from env import creds, text


def top_secret(channel):
    """
              Args:
                  channel (str): Name of channel to send card to. Currently 1 option
              Returns:
                  (str): The channel's webhook as url string
              """
    # currently only 1 channel is setup. This will be added in future versions need
    if channel == 'test':
        return creds.testhook
    elif channel == 'programming':
        return creds.programminghook
    elif channel == 'West-project':
        return creds.westcoasthook
    else:
        print ( text.no_channel )
        return creds.testhook


class Send_Hook:
    def __init__(self, channel, temp_project, file_path):
        """
                  Args:
                      channel (str): Which team to send card to. Currently 1 option
                      file_path (str): 'Path to json being Posted'
                  Returns:
                      (str): Post error message
                  """
        # converts channel name to url from creds file
        self.channel = top_secret ( channel )
        self.project = temp_project
        self.file = file_path
        with open ( self.file + '_card.json', 'r' ) as f:
            file = f.read ()
        self.finished_card = json.loads ( file )
        self.draft_message ()

    def draft_message(self):
        # prompt user to review card.
        # TODO: build Interactive module
        # TODO: find way to display preview
        print ( self )
        self.send_message ()

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


if __name__ == '__main__':
    file_path = "C:\\Users\\Dan.Edens\\Desktop\\Tree\\the_lab\\Python\\pyppeteer_sitecheck_scrapper\\env\\data\\cards" \
                "\\Test_Project"
    project = "Test_Project"
    Send_Hook ( 'test', project, file_path )
