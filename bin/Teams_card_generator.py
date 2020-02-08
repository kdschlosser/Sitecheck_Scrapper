# """Teams_card_generator.py: Library for generating JSON cards from a template.
# Guide on Message Cards: https://poszytek.eu/en/microsoft-en/microsoft-message-cards-the-ultimate-guide/
# Change Log:
# 2/2/2020
# Adds the card_template class
# Adds the factory class
#
#
# """

import json

from env import text

# __author__ = "Dan Edens"
# __version__= "0.3.0"

global storage
storage = text.ROOT_dir + "\\data\\cards\\"
print(storage)


# TODO: Rebuild template model to messagecard
class _template:
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


def store ( project, data_list ):
    """
            Args:
                project (str): from self.project.name
                data_list (list): ['IP2', 'good', 'Okay', '2020-01-16 08:00:00']

            Returns:
                none
            """
    file_path = storage + project + '_temp.txt'
    with open(file_path, 'a') as file:
        if file.tell() == 0:
            file.write('[')
        else:
            file.write(',')
        file.write(json.dumps(data_list))


class sensor_data:
    def __init__ ( self, name, color, status, time ):
        """
		        Args:
		            name (str):
		            color (str): 'good','attention','warning'
		            status (str): 'Okay', 'Behind', 'Older than a week'
		            time (str) '2020-01-14 08:00:00'
		        Returns:
		        	string
		        """
        self.name = name
        self.color = color
        self.status = status
        self.time = time

    def __str__ ( self ):
        # Formats the Sensor_data into table rows
        data_line = _template.st1 + self.name + _template.st2 + self.status + _template.st3 + self.color + _template.st4 + self.time + _template.st5
        return str(data_line)


class generator:
    def __init__ ( self, current_project ):
        """
		        Args:
		            current_project (object):
		            list_of_sensor_data (list):

		        """
        # Name to display at top of card
        self.project = current_project.name
        # File path of output file
        # Location of staged output. It will than be picked up by the Teams_hook.py
        # On card button click
        self.store_path = storage + current_project.name + '_temp.txt'
        self.generator_output = storage + current_project.name + "_card.json"
        self.url = current_project.url
        # this is the list each sensor's data was appended to while scanning
        # self.data = list_of_sensor_data

    def compile_data ( self ):
        # Adds the end bracket to finish list of lists
        with open(self.store_path, 'a') as file:
            file.write(']')
        # Reads the finished product as string
        with open(self.store_path) as file:
            list_of_lists = file.read()
        # Converts String to List
        card_list = json.loads(list_of_lists)
        # Sends final copy of list to the generator
        return self.generate_template(card_list)

    def generate_template ( self, card_list ):
        with open(self.generator_output, 'w') as gen_file:
            # print(gen_file.name)
            # Builds the Teams Card
            # Traditional methods of Json formatting do not preserve the template's syntax
            # Add the sensor table section goes above the sensors,
            # For each current_project held in data, add a line to the card containing it's data
            print(_template.Top_prefix1 + self.project + _template.Top_prefix2, file=gen_file)
            print(_template.sensor_prefix, file=gen_file)
            _run = len(card_list)
            _loop = 0
            for e in card_list:
                #              # data = [name, color, status, time]
                data_info = sensor_data(e[0], e[1], e[2], e[3])
                _loop += 1
                if _loop != _run:
                    # Add each sensor to the card and add a comma between them.
                    print(str(data_info) + ',', file=gen_file)
                else:
                    # Once the last item is added it will add without the final comma
                    # Add the bits to close up the table.
                    print(data_info, file=gen_file)
            print(_template.sensor_suffix, file=gen_file)
            # TODO: this row needs more development, It will house links to troubleshooting tools
            print(_template.Link_row_Template1 + self.project + _template.Link_row_Template2,
                  file=gen_file)
            # TODO: this row needs more development, It will house buttons
            # Add the bits to close up the card.
            # TODO: queue or start teams_hook.py
            print(_template.button_row_template1 + 'https://www.google.com/' + _template.button_row_template2,
                  file=gen_file)
            print(_template.Bot_suffix, file=gen_file)
        return gen_file.name
