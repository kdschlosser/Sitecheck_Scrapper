'''
This is an example of how to send data to Team's webhooks in Python with the
requests module.
Documentation for Team's Incoming Webhooks:
https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/what-are-webhooks-and-connectors

'''

import json
import requests
import os
# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/

webhook_url = 'https://webhook.site/854c483a-1a38-4523-b25e-0bb46012a101'
Watchdog_data = os.environ['cardtest1.json']  
#path to card's json file. use "setx sitecheckdata '%userprofile%/desktop/path/to/file'"

response = requests.post(
    webhook_url, data=json.dumps(Watchdog_data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to Teams returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )
