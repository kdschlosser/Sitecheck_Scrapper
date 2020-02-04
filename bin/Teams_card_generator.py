# """Teams_card_generator.py: Library for generating JSON cards from a template.
# Change Log:
# 2/2/2020
# Adds the card_template class
# Adds the factory class
#
#
# """

# __author__ = "Dan Edens"
# __version__= "0.2.0"
import json
import os

ROOT_DIR = os.path.dirname ( os.path.abspath ( __file__ ) )
global storage
storage = ROOT_DIR + "/env/data/cards/"


class card_template:
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
    # + project +
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
    # project_url. This section needs work
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
    # + project url +
    button_row_template2 = '''"
						}
			}'''
    Bot_suffix = '''	],
		"$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
		"version": "1.0"
	}'''


def store(project, data_list):
    """
            Args:
                project (str): from self.project.name
                data_list (list): ['IP2', 'good', 'Okay', '2020-01-16 08:00:00']

            Returns:
                none
            """
    file_path = storage + project + '_temp.txt'
    if os.path.exists ( file_path ):
        with open ( file_path, 'a' ) as file:
            # If file exists before now, this adds a comma between lists
            file.write ( ',' )
            file.write ( json.dumps ( data_list ) )
    else:
        with open ( file_path, 'w' ) as file:
            file.write ( '[' )
            file.write ( json.dumps ( data_list ) )


class sensor_data:
    def __init__(self, name, color, status, time):
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

    def __str__(self):
        # Formats the Sensor_data into table rows
        data_line = card_template.st1 + self.name + card_template.st2 + self.status + card_template.st3 + self.color + card_template.st4 + self.time + card_template.st5
        return str ( data_line )


class generator:
    def __init__(self, current_project):
        """
		        Args:
		            current_project (object):
		            list_of_sensor_data (list):

		        """
        # Name to display at top of card
        self.project = current_project.name
        # File path of output file
        self.file_path = storage + current_project.name
        # Location of staged output. It will than be picked up by the Teams_hook.py
        self.file = storage + "\\" + current_project.name + ".json"
        # On card button click
        self.url = current_project.url
        # this is the list each sensor's data was appended to while scanning
        # self.data = list_of_sensor_data

        # self.generate_template ( self )

    def compile_data(self):
        # Adds the end bracket to finish list of lists
        with open ( self.file_path + '_temp.txt', 'a' ) as file:
            file.write ( ']' )
        # Reads the finished product as string
        with open ( self.file_path + '_temp.txt', 'r' ) as file:
            list_of_lists = file.read ()
        # Converts String to List
        card_list = json.loads ( list_of_lists )
        # Sends final copy of list to the generator
        self.generate_template ( self, card_list )

    def generate_template(self, card_list):
        # Builds the Teams Card
        # Traditional methods of Json formatting do not preserve the template's syntax
        print ( card_template.Top_prefix1 + self.project + card_template.Top_prefix2, self.file_path + '_card.json' )
        # Add the sensor table section goes above the sensors,
        print ( card_template.sensor_prefix, self.file_path + '_card.json' )
        # For each current_project held in data, add a line to the card containing it's data
        _run = len ( card_list )
        _loop = 0
        for e in card_list:
            #              # data = [name, color, status, time]
            data_info = sensor_data ( e[0], e[1], e[2], e[3] )
            _loop += 1
            if _loop != _run:
                # Add each sensor to the card and add a comma between them.
                print ( data_info + ',', self.file_path + '_card.json' )
            else:
                # Once the last item is added it will add without the final comma
                print ( data_info, self.file_path + '_card.json' )
        # Add the bits to close up the table.
        print ( card_template.sensor_suffix, self.file_path + '_card.json' )
        # TODO: this row needs more development, It will house links to troubleshooting tools
        print ( card_template.Link_row_Template1 + project + card_template.Link_row_Template2,
                self.file_path + '_card.json' )
        # TODO: this row needs more development, It will house buttons
        print ( card_template.button_row_template1 + project.url + card_template.button_row_template2,
                self.file_path + '_card.json' )
        # Add the bits to close up the card.
        print ( card_template.Bot_suffix, self.file_path + '_card.json' )
        # TODO: queue or start teams_hook.py

# Testing values
if __name__ == 'Teams_card_generator':
    project = []
    project.name = 'Sample Project'
    project.url = 'https://quickview.geo-instruments.com'
    list_of_sensor_data = [['IP1', 'attention', 'Behind', '2020-01-14 08:00:00'],
                           ['IP2', 'good', 'Okay', '2020-01-16 08:00:00'],
                           ['IP3', 'warning', 'Older than a week', '2020-01-04 08:00:00']]
    # generator ( project, list_of_sensor_data )
