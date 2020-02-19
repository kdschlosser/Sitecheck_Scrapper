# -*- coding: utf-8 -*-

"""
This file is part of the **pyppeteer_sitecheck_scrapper**
project git@geodev.geo-instruments.com:DanEdens/pyppet_sitecheck_scrapper.git

:platform: Windows
:license:
:synopsis: teams_card_generator.py: Library for generating JSON cards from a template.
	Guide on Message Cards: https://docs.microsoft.com/en-us/adaptive-cards/

	This Collects stored sensor data and generates a Microsoft Team's Adaptive Card.

.. moduleauthor::  Dan Edens @DanEdens <Dan.Edens@geo-instruments.com>
"""

# __author__ = "Dan Edens"
# __email__ = "Dan.Edens@Geo-Instruments.com"
# __status__ = "Overhaul"
# __version__= "0.4.2"

import json
from ..env import text


def store(project, data_list):
	"""
	:param project:	Project name
	:type project: str

	:param data_list: Sensor data in list format
		Examples: ['IP2', 'good', 'Okay', '2020-01-16 08:00:00']
	:type data_list: list

	:rtype: None
	"""
	file_path = text.ROOT_card+project+'_temp.txt'
	with open(file_path, 'a') as file:
		if file.tell() == 0:
			file.write('[')
		else:
			file.write(',')
		file.write(json.dumps(data_list))


class SensorData:
	"""
	Class to hold the data from the sensor.
	"""

	def __init__(self, name, color, status, time):
		"""
		Constructor

		:param name: Sensor ID
		:type name: str

		:param color: Examples:'good','attention','warning'
		:type color: str

		:param status: Examples:'Okay', 'Behind', 'Older than a week'
		:type status: str

		:param time: Examples: '2020-01-14 08:00:00'
		:type time: str


		:returns:(sudo json)
			Sensor data in Card format block
		:rtype: str
		"""
		self.name = name
		self.color = color
		self.status = status
		self.time = time

	@property
	def as_dict(self):
		# Formats the Sensor_data into table rows
		data = dict(
			spacing="small",
			type="ColumnSet",
			columns=[
				_column(text=self.name),
				_column(text=self.status, color=self.color),
				_column(text=self.time),
			]
		)

		return data


def _column(**params):
	if params:
		return dict(type="Column", width="stretch", items=[_text_block(**params)])
	else:
		return dict(type="Column", width="stretch")


def _padding(top=None, bottom=None):
	return dict(top=top, left="default", bottom=bottom, right="default")


def _text_block(**params):
	return params.update(dict(type="TextBlock"))


class Generator(object):
	"""
	After the Site is scanned, the collected data is processed into a Team's channel card
	"""

	def __init__(self, current_project):
		"""
		Constructor

		:param current_project: current project class instance
		:type current_project: TBD


		project (str): Name to display at top of card
		store_path (str): Location of staged output. It will than be picked up by the Teams_hook.py
		generator_output (str): File path of output file
		url (str): Card button 'Website" link target
		"""
		self.project = current_project.name
		self.store_path = text.ROOT_card+current_project.name+'_temp.txt'
		self.generator_output = text.ROOT_card+current_project.name+"_card.json"
		self.url = current_project.url

	def compile_data(self):
		"""
		Adds the end bracket to finish list of lists

		Reads the finished product as string
		Converts String to List
		Sends final copy of list to generate_template

		:returns: path and filename for compiled json data
		:rtype: str
		"""
		with open(self.store_path, 'a') as file:
			file.write(']')
		with open(self.store_path) as file:
			list_of_lists = file.read()
		card_list = json.loads(list_of_lists)
		return self.generate_template(card_list)

	def generate_template(self, card_list):
		"""
		Builds the Teams Card

		Traditional tools for Json formatting do not preserve the template's syntax,
		So it has to be built manually
		For card_list, the sensor data is looped to create a table.
		This adds each sensor to the card and add a comma between them.
		Once the last run, the comma is skipped and the bracket is closed

		Notes:
			Using print to write is convenient insurance against missing
			line breaks when manually building json or xml templates
			To add a new variable,split current template into
			2 at that location and combine as string

		:param card_list: List of sensor data in card template format [[name, color, status, time]]
		:type card_list: 2 dimensional list [[str, str, str, str]]

		:returns: path and filename of generated json file
		:rtype: str
		"""
		output = dict(
			hideOriginalBody=True,
			type="AdaptiveCard",
			padding=None,
			body=[
				dict(
					type="ColumnSet",
					padding=_padding(top="default"),
					columns=[
						dict(
							type="Column",
							verticalContentAlignment="Center",
							items=[
								_text_block(
									verticalContentAlignment="Center",
									horizontalAlignment="Center",
									size="Large",
									text="Site Check Scanner",
									isSubtle=True
								)
							],
							width="stretch"
						),
						dict(
							type="Column",
							verticalContentAlignment="Center",
							items=[
								dict(
									verticalContentAlignment="Center",
									type="Image",
									url=(
										"https://cdn1.imggmi.com/uploads/2020/1/16/"
										"fc83bdfc3949e70df506c972948d68d3-full.png"
									),
									width="80px",
									altText="Geo Logo"
								)
							],
							width="auto"
						)
					]
				),
				dict(
					separator=True,
					spacing="medium",
					type="Container",
					padding=_padding(),
					items=[
						_text_block(size="Medium", weight="Bolder", text=self.project),
						_text_block(text="Below are the sensors that need to be looked into.", wrap=True)
					]
				),
				dict(
					type="Container",
					spacing="small",
					padding=_padding(),
					# sensor data
					items=[SensorData(e[0], e[1], e[2], e[3]).as_dict for e in card_list]
				),
				dict(
					spacing="small",
					type="Container",
					style="emphasis",
					padding=_padding("small", "small"),
					items=[
						dict(
							type="ColumnSet",
							columns=[
								_column(weight="Bolder", text=self.project),
								_column(),
								_column(weight="Bolder", text="")
							]
						)
					]
				),
				dict(
					type="Container",
					padding=_padding(bottom="default"),
					items=[dict(type="TextBlock", weight="Bolder", text="Project Website")],
					selectAction=dict(
						type="Action.OpenUrl",
						title="View Monday",
						url="https://www.google.com/"
					)
				)
			],
			version="1.0"
		)
		output = output.update({"$schema": "http://adaptivecards.io/schemas/adaptive-card.json"})

		with open(self.generator_output, 'w') as gen_file:
			gen_file.write(json.dumps(output, indent=4))

		return gen_file.name
