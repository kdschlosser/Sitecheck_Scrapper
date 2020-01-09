debug = 0
import os, sys
from datetime import datetime

today = datetime.today()
nowdate = today.strftime("%Y-%m-%d %H:%M:%S")
filedate = today.strftime("%Y-%m-%d")

pathtonote = os.path.abspath(os.path.dirname(sys.argv[0])) + '/_' + filedate + '/Notes.txt'
outputfile = '_sitecheck.txt'
pathtoWarnfile = '_WatchdogFile.txt'
pathtoOldfile = '_Watchdog_Old.txt'	
outputjson = ''
fileheader = 'Sitecheck Scan for: ' + filedate + '\nProject: '
uptoDate = 'Most recent data is within 24 hours\n'
behindDate = 'Instrument is behind\n'
oldDate = 'Reading has been missing for over a week\n'
scanplan = '\nScanning plan views:'
postloginmessage = 'Login Successful.'
usage_argdesc = 'Usage: --debug=[1,2,3] -p <project> -o %date_<filename>.txt'
help_argdesc = ''
version_argdesc = 'Version: ' 
project_argdesc = 'project=<projectname> Project to scan'
output_argdesc = "output=<_filename.txt> output file name. \nOutput file Default value is: \'_sitecheck.txt\'"
setup_argdesc = 'Input project name from the Amp URL. <--projectname=newtreehouse> <--other options to add later when i make generator>'
debug_argdesc = 'Run tests without web requests and redirect from file output to console.'
watchlisttxt = "Watchdog alert list:\n"
oldlisttxt = "Watchdog alert items older than a week:\n"
filerefreshed = 'Creating File...'

if debug == 0:
	loginmessage = '\nRunning scan on Planview: '
	hasSitemessage = 'This project is housed on: '
	exitmessage = 'Scan completed.'
	# sensorarray = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112','111','114','115','116','117','118','119','120','121','122','121','124','125','126','127','128','129','130','131','132','131','134','135','136','137','138','139','140','141','142','141','144','145','146','147','148','149','150','151','152','151','154','155','156','157','158','159','160','161','162','161','164','165','166','167','168','169','170','171','172','171','174','175','176','177','178','179','180','181','182','181','184','185','186','187','188','189','190','191','192','191','194','195','196','197','198','199','200','201','202','201','204','205','206','207','208','209','210','211','212','211','214','215','216','217','218','219','220','221','222','221','224','225','226','227','228','229','230','231','232','231','234','235','236','237','238','239','240','241','242','241','244','245','246','247','248','249','250','251','252','251','254','255','256','257','258','259','260','261','262','261','264','265','266','267','268','269','270','271','272','271','274','275','276','277','278','279','280','281','282','281','284','285','286','287','288','289','290','291','292','291','294','295','296','297','298','299','300','301','302','301','304','305','306','307','308','309']
	# head = 'headless: true'
	head = 'headless: true'
elif debug == 1:
	loginmessage = '\nPV:'
	hasSitemessage = ''
	exitmessage = 'Test end'
	# sensorarray = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112','111','114','115','116','117','118','119','120','121','122','121','124','125','126','127','128','129','130','131','132','131','134','135','136','137','138','139','140','141','142','141','144','145','146','147','148','149','150','151','152','151','154','155','156','157','158','159','160','161','162','161','164','165','166','167','168','169','170','171','172','171','174','175','176','177','178','179','180','181','182','181','184','185','186','187','188','189','190','191','192','191','194','195','196','197','198','199','200','201','202','201','204','205','206','207','208','209','210','211','212','211','214','215','216','217','218','219','220','221','222','221','224','225','226','227','228','229','230','231','232','231','234','235','236','237','238','239','240','241','242','241','244','245','246','247','248','249','250','251','252','251','254','255','256','257','258','259','260','261','262','261','264','265','266','267','268','269','270','271','272','271','274','275','276','277','278','279','280','281','282','281','284','285','286','287','288','289','290','291','292','291','294','295','296','297','298','299','300','301','302','301','304','305','306','307','308','309']
	# head = 'headless: false'
	head = 'headless: true'
elif debug ==2:
	loginmessage = '\nPV:'
	hasSitemessage = ''
	exitmessage = 'Break reached, No errors'
	# sensorarray = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112','111','114','115','116','117','118','119','120','121','122','121','124','125','126','127','128','129','130','131','132','131','134','135','136','137','138','139','140','141','142','141','144','145','146','147','148','149','150','151','152','151','154','155','156','157','158','159','160','161','162','161','164','165','166','167','168','169','170','171','172','171','174','175','176','177','178','179','180','181','182','181','184','185','186','187','188','189','190','191','192','191','194','195','196','197','198','199','200','201','202','201','204','205','206','207','208','209','210','211','212','211','214','215','216','217','218','219','220','221','222','221','224','225','226','227','228','229','230','231','232','231','234','235','236','237','238','239','240','241','242','241','244','245','246','247','248','249','250','251','252','251','254','255','256','257','258','259','260','261','262','261','264','265','266','267','268','269','270','271','272','271','274','275','276','277','278','279','280','281','282','281','284','285','286','287','288','289','290','291','292','291','294','295','296','297','298','299','300','301','302','301','304','305','306','307','308','309']
	head = 'headless: false'
	# head = 'headless: true'
elif debug == 3:
	loginmessage = '\nPV:'
	hasSitemessage = ''
	exitmessage = 'Break reached, No errors'
	# sensorarray = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112','111','114','115','116','117','118','119','120','121','122','121','124','125','126','127','128','129','130','131','132','131','134','135','136','137','138','139','140','141','142','141','144','145','146','147','148','149','150','151','152','151','154','155','156','157','158','159','160','161','162','161','164','165','166','167','168','169','170','171','172','171','174','175','176','177','178','179','180','181','182','181','184','185','186','187','188','189','190','191','192','191','194','195','196','197','198','199','200','201','202','201','204','205','206','207','208','209','210','211','212','211','214','215','216','217','218','219','220','221','222','221','224','225','226','227','228','229','230','231','232','231','234','235','236','237','238','239','240','241','242','241','244','245','246','247','248','249','250','251','252','251','254','255','256','257','258','259','260','261','262','261','264','265','266','267','268','269','270','271','272','271','274','275','276','277','278','279','280','281','282','281','284','285','286','287','288','289','290','291','292','291','294','295','296','297','298','299','300','301','302','301','304','305','306','307','308','309']
	head = 'headless: false'
	# head = 'headless: true'