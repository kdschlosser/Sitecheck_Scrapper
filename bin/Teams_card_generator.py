
# """Teams_card_generator.py: Library for generating JSON cards from a template."""

# __author__ = "Dan Edens"
# __version__= "0.0.1"

import json
import sys
import card_template as ctem
from datetime import datetime, timedelta

project = 'Audi Central Houston'
project_url = 'https://audicentralhouston.geo-instruments.com/index.php'
Sensor_name = ''
Sensor_time = ''
Sensor_status = ''
Sensor_status_color = 'attention'
warning_results = []
data = [['IP1','attention', 'Behind','2020-01-14 08:00:00'],['IP2','good', 'Okay','2020-01-16 08:00:00'],['IP3','warning', 'Older than a week','2020-01-04 08:00:00']]


class dataItem:
	def __init__(self, name, color, status, time):
		self.name = name
		self.color = color
		self.status = status
		self.time = time
	
	def __str__(self):
		dataline = ctem.st1 + self.name + ctem.st2 + self.status + ctem.st3 + self.color + ctem.st4 + self.time + ctem.st5
		return dataline

print(ctem.Top_prefix1+project+ctem.Top_prefix2)

print(ctem.sensor_prefix)
l = len(data)
r = 0
for e in data:
	data_info = dataItem(e[0],e[1],e[2],e[3])
	r += 1
	if r != l:
		print(str(data_info)+',')
	else:
		print(str(data_info))

print(ctem.sensor_suffix)

print(ctem.Link_row_Template1 + project + ctem.Link_row_Template2)

print(ctem.button_row_template1 + project_url + ctem.button_row_template2)

print(ctem.Bot_suffix)