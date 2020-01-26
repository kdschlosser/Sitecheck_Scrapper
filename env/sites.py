
outputfile = '_sitecheck.txt'
watchdog = 86400000
watchlimit = watchdog * 7
parallel = 1

# class selectors:
class ampAdmin:
	url: "http =//ampadmin.geo-instruments.com/geoadmin.php"

class amp:
	name = 'amp'
	urlstring = '.geo-instruments.com/index.php'
	logincss = '#s_text_login_name'
	pwcss = '#s_password_login_password'
	loginbutton = 'body > div > form > input.button'
	planview = '?s_cat=project&i_project=17&i_planview='
	all_pre = 'body > div:nth-child('
	all_presuf = ') > div:nth-child('
	label = ['3','4']
	plot = '?s_cat=plot_info&s_url='
	title = ') > a:nth-child(1)'
	sensor = ') > a:nth-child(3)'
	vmhealth = ') > a:nth-child(5)'

class qv:
		name = 'qv'
		urlstring = 'https://quickview.geo-instruments.com/login.php'
		logincss = '#user'
		pwcss = '#pass'
		loginbutton = '#login > form > button'
		projects = '#menuProjects'
		proj_pre = 'div#projectList div:nth-child('
		proj_post = ') > div.panelRowTxt2'
		views = 'li#menuViews p'
		thumb = '#thumb'
		scrollbar = 'body > div.wrapper > div.sidePanel.ui-resizable > div.ui-resizable-handle.ui-resizable-e'
		scrollbar2 = 'div#viewList'
		# scrollbar = 'div#projectSearch > select'
		# scrollbar = 'div.sidePanel.ui-resizable > div.panelHeading'
		hoverbox = "#hoverBox"

class trulook:
	name = 'truelook'
	urlstring = '.geo-instruments.com/index.php'
	logincss = 'input#tl_login_username'
	pwcss = 'input#tl_login_password'
	loginbutton = 'keyboard.press(\'Enter\')' #broken
	planview = 'img#tl_live_image'
