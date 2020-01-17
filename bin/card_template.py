#Project
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