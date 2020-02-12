"""
teams_card_generator.py: Library for generating JSON cards from a template.
Guide on Message Cards: https://docs.microsoft.com/en-us/adaptive-cards/

This Collects stored sensor data and generates a Microsoft Team's Adaptive Card.
"""
# __author__ = "Dan Edens"
# __version__= "0.4.1"

import json

from env import text


def store(project, data_list):
    """
        Args:
            project (str): Project name
            data_list (list): Sensor data in list format
                Examples: ['IP2', 'good', 'Okay', '2020-01-16 08:00:00']
        Returns:
            (none)
    """
    file_path = text.ROOT_card+project+'_temp.txt'
    with open(file_path, 'a') as file:
        if file.tell() == 0:
            file.write('[')
        else:
            file.write(',')
        file.write(json.dumps(data_list))


class Sensor_Data:
    """
            # TODO fill this in
    """

    def __init__(self, name, color, status, time):
        """
            Args:
                name (str): Sensor ID
                color (str):
                    Examples:'good','attention','warning'
                status (str):
                    Examples:'Okay', 'Behind', 'Older than a week'
                time (str):
                    Examples: '2020-01-14 08:00:00'
            Returns (str): (sudo json)
                Sensor data in Card format block
        """
        self.name = name
        self.color = color
        self.status = status
        self.time = time

    def __str__(self):
        # Formats the Sensor_data into table rows
        data_line = Template.st1+self.name+Template.st2+self.status+Template.st3+self.color+Template.st4+self.time+Template.st5
        return str(data_line)


class Generator:
    """
        After the Site is scanned, the collected data is processed into a
        Team's channel card
            Args:
                current_project (obj): Project Object
    """

    def __init__(self, current_project):
        """
            Creates (self):
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
                Returns: (str)
                    self.generator_output
                    gen_file.name - name of generated json file
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
                Args:
                    card_list (list): List of sensor data in card template format
                        card_list = [name, color, status, time]
                Returns (str):
                    gen_file.name - name of generated file

            Notes:
                Using print to write is convenient insurance against missing
                line breaks when manually building json or xml templates

                To add a new variable,split current template into
                2 at that location and combine as string
        """
        with open(self.generator_output, 'w') as gen_file:
            print(Template.Top_prefix1+self.project+Template.Top_prefix2, file=gen_file)
            print(Template.sensor_prefix, file=gen_file)
            _run = len(card_list)
            _loop = 0
            for e in card_list:
                data_info = Sensor_Data(e[0], e[1], e[2], e[3])
                _loop += 1
                if _loop != _run:
                    print(str(data_info)+',', file=gen_file)
                else:
                    print(data_info, file=gen_file)
            print(Template.sensor_suffix, file=gen_file)
            print(Template.Link_row_Template1+self.project+Template.Link_row_Template2, file=gen_file)
            print(Template.button_row_template1+'https://www.google.com/'+Template.button_row_template2, file=gen_file)
            print(Template.Bot_suffix, file=gen_file)
        return gen_file.name


class Template:
    Top_prefix1 = '''{
    		"hideOriginalBody": true,
    		"type": "AdaptiveCard",
    		"padding": "none",
    		"body": [
			{
				"type": "ColumnSet",
				"padding": {
					"top": "default",
					"left": "default",
					"bottom": "none",
					"right": "default"
				},
				"columns": [
					{
						"type": "Column",
						"verticalContentAlignment": "Center",
						"items": [
							{
								"type": "TextBlock",
								"verticalContentAlignment": "Center",
								"horizontalAlignment": "Center",
								"size": "Large",
								"text": "Site Check Scanner",
								"isSubtle": true
							}
						],
						"width": "stretch"
					},
					{
						"type": "Column",
						"verticalContentAlignment": "Center",
						"items": [
							{
								"verticalContentAlignment": "Center",
								"type": "Image",
								"url": "https://cdn1.imggmi.com/uploads/2020/1/16/fc83bdfc3949e70df506c972948d68d3-full.png",
								"width": "80px",
								"altText": "Geo Logo"
							}
						],
						"width": "auto"
					}
				]
			},
			{
				"separator": true,
				"spacing": "medium",
				"type": "Container",
				"padding": {
					"top": "none",
					"left": "default",
					"bottom": "none",
					"right": "default"
				},
				"items": [
					{
						"type": "TextBlock",
						"size": "Medium",
						"weight": "Bolder",
						"text": "'''
    Top_prefix2 = '''"
					},
					{
						"type": "TextBlock",
						"text": "Below are the sensors that need to be looked into.",
						"wrap": true
					}
				]
			},'''
    sensor_prefix = '''		{
				"type": "Container",
				"spacing": "small",
				"padding": {
					"top": "none",
					"left": "default",
					"bottom": "none",
					"right": "default"
				},
				"items": ['''
    st1 = '''				{
						"spacing": "small",
						"type": "ColumnSet",
						"columns": [
							{
								"type": "Column",
								"width": "stretch",
								"items": [
									{
										"type": "TextBlock",
										"text": "'''
    st2 = '''"
									}
								]
							},
							{
								"type": "Column",
								"width": "stretch",
								"items": [
									{
										"type": "TextBlock",
										"text": "'''
    st3 = '''",
										"color": "'''
    st4 = '''"
									}
								]
							},
							{
								"type": "Column",
								"width": "stretch",
								"items": [
									{
										"type": "TextBlock",
										"text": "'''
    st5 = '''"
									}
								]
							}
						]
					}'''
    sensor_suffix = '''			]
			},'''
    Link_row_Template1 = '''		{
				"spacing": "small",
				"type": "Container",
				"style": "emphasis",
				"padding": {
					"top": "small",
					"left": "default",
					"bottom": "small",
					"right": "default"
				},
				"items": [
					{
						"type": "ColumnSet",
						"columns": [
							{
								"type": "Column",
								"items": [
									{
										"type": "TextBlock",
										"weight": "Bolder",
										"text": "'''
    Link_row_Template2 = '''"
									}
								],
								"width": "stretch"
							},
							{
								"type": "Column",
								"width": "stretch"
							},
							{
								"type": "Column",
								"items": [
									{
										"type": "TextBlock",
										"weight": "Bolder",
										"text": ""
									}
								],
								"width": "stretch"
							}
						]
					}
				]
			}'''
    button_row_template1 = ''',
			{
				"type": "Container",
				"padding": {
					"top": "none",
					"left": "default",
					"bottom": "default",
					"right": "default"
				},
				"items": [
					{
						"type": "TextBlock",
						"weight": "Bolder",
						"text": "Project Website"
					}
				],
						"selectAction": {
							"type": "Action.OpenUrl",
							"title": "View Monday",
							"url": "'''
    button_row_template2 = '''"
						}
			}'''
    Bot_suffix = '''	],
		"$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
		"version": "1.0"
	}'''
