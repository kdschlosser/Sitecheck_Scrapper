
outputfile = '_sitecheck.txt'
watchdog = 86400000
watchlimit = watchdog * 7
parallel = 1

class selectors:
	class amp: 
		name: 'amp'
		urlstring: '.geo-instruments.com/index.php'
		logincss: '#s_text_login_name'
		pwcss: '#s_password_login_password'
		loginbutton: 'body > div > form > input.button'
		planview: '?s_cat=project&i_project=17&i_planview='
		all_pre: 'body > div:nth-child('
		all_presuf: ') > div:nth-child('
		label: ['3','4']
		plot: '?s_cat=plot_info&s_url='
		title: ') > a:nth-child(1)'
		sensor: ') > a:nth-child(3)'
		vmhealth: ') > a:nth-child(5)'

class qv: 
		name: 'qv'
		urlstring: 'https://quickview.geo-instruments.com/login.php'
		logincss: '#user'
		pwcss: '#pass'
		loginbutton: '#login > form > button'
		menuprojects: '#menuProjects'
		Qvprojectpre: 'div#projectList div:nth-child('
		Qvprojectpost: ') > div.panelRowTxt2'
		views: 'li#menuViews p'
		thumb: '#thumb'
		scrollbar: 'body > div.wrapper > div.sidePanel.ui-resizable > div.ui-resizable-handle.ui-resizable-e'
		scrollbar2: 'div#viewList'
		# scrollbar: 'div#projectSearch > select'
		# scrollbar: 'div.sidePanel.ui-resizable > div.panelHeading'
		hoverbox: "#hoverBox"

class trulook:
	name: 'truelook'
	urlstring: '.geo-instruments.com/index.php'
	logincss: 'input#tl_login_username'
	pwcss: 'input#tl_login_password'
	loginbutton: 'keyboard.press(\'Enter\')' #broken
	planview: 'img#tl_live_image'



# module.exports = {
# 	amp,
# 	qv,
# 	trulook,
# 	parallel,
# 	watchdog,	
# 	watchlimit,
# 	urlstring: '.geo-instruments.com/index.php',
# 	outputfile,
#     sensorarray: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112','111','114','115','116','117','118','119','120','121','122','121','124','125','126','127','128','129','130','131','132','131','134','135','136','137','138','139','140','141','142','141','144','145','146','147','148','149','150','151','152','151','154','155','156','157','158','159','160','161','162','161','164','165','166','167','168','169','170','171','172','171','174','175','176','177','178','179','180','181','182','181','184','185','186','187','188','189','190','191','192','191','194','195','196','197','198','199','200','201','202','201','204','205','206','207','208','209','210','211','212','211','214','215','216','217','218','219','220','221','222','221','224','225','226','227','228','229','230','231','232','231','234','235','236','237','238','239','240','241','242','241','244','245','246','247','248','249','250','251','252','251','254','255','256','257','258','259','260','261','262','261','264','265','266','267','268','269','270','271','272','271','274','275','276','277','278','279','280','281','282','281','284','285','286','287','288','289','290','291','292','291','294','295','296','297','298','299','300','301','302','301','304','305','306','307','308','309']
