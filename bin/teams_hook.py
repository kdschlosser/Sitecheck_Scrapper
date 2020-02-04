'''
This sends completed cards through a webhook to a specific Team's channel (Team)
Documentation for Team's card incoming Webhooks:
https://docs.microsoft.com/en-us/micrsoftteams/platform/webhooks-and-connectors/what-are-webhooks-and-connectors

'''

import json

import requests

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/

webhook_url = 'https://webhook.site/854c483a-1a38-4523-b25e-0bb46012a101'


class Send_Hook:
    def __init__(self, channel, file_path):
        self.channel = channel
        self.file = file_path

    def draft_message(self):
        self.finished_card = json.loads ( self.file + '_card.json' )

    def send_message(self):
        response = requests.post (
            webhook_url, data=json.dumps ( self.finished_card ),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError (
                'Request to Teams returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
