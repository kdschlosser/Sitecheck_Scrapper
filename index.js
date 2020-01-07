//Daily Sitecheck Web Scrapper V. 3.7.3
const puppeteer = require('puppeteer');
const fs = require('fs');
const argv = require('yargs').argv;
const nconf = require('nconf');
const csv = require('csv')
const readline = require('readline');
const LOCAL = require(__dirname + '/env/sites');
const TEXT = require(__dirname + '/env/text');
require('events').defaultMaxListeners = 25;

if (argv.user)    	{user = argv.user} 			else {user = 'dan.edens'};  // -u
if (argv.debug)    	{debug = argv.debug}		else {debug = 0}; // -d
if (argv.parallel) 	{parallel = argv.parallel}	else {parallel = LOCAL.parallel}; // -p
if (argv.verbose)  	{verbose = true}			else {verbose = false}; // -v
if (argv.check)    	{check = true} 				else {check = false}; // -c
if (argv.getvalue)  {getvalue = true}			else {getvalue = false}; // -g
if (argv.preformance){preformance = true}		else {preformance = false}; // -s
if (argv.watchdog)  {watchdog = argv.watchdog}	else {watchdog = 86400000}; const watchlimit = watchdog * 7; // -w
if (argv.creds)     {creds = argv.creds}		else {creds = '/users/dan.edens/creds'}; CREDS = require(__dirname + creds); //For loading clients login in.

function group(msg) {if(debug > '0') {console.group('Group: ' + msg)}};
function groupend(msg) {if(debug > '0') {console.groupEnd(); console.log('G End: ' + msg + '\n')}};
function verboselog(msg) {if (verbose) {Debug.print(msg,)}};


class Debug {
	static async print(data, file) {
		if (preformance) {console.log(new Date().toISOString())};
		if (file) {} else {file = 'Log.txt'};
		try {
			if(debug == 0) {
				file.write(data);
			} else if (debug == 1) {
				console.log(data);
				file.write(data);
			} else if (debug == 2) {
				group('Debug print - Output');
				console.log(data);
				groupend('Debug print - Output')
			} else if (debug == 3) {};
			} catch(error) {
				console.log('Caught:', error.message)
			};
		if (preformance) {console.log(new Date().toISOString())};
	};
	static async askQuestion(query) {
		const rl = readline.createInterface({
			input: process.stdin,
			output: process.stdout,
		});
		return new Promise(resolve => rl.question(query, ans => {
			rl.close();
			verboselog(ans);
			resolve(ans);
		}))
	}
	static async checkExists(file){
		let time=new Date().toISOString();
		let promises = [];
		file.forEach(function(item) {
			try {fs.promises.access(item)
				//Something something appead a number to each filename
				//parse ending value of item if #s
				//let newitem = itemvalue+1
				// return newitem; //rerun checkExists
			} catch (ENOENT) {
				console.log('Created File at:\n' + item);
				fs.writeFileSync(item, 'Created on: ' + time, { flag: 'w'},
					function (err) {if (err) throw err})
					return};
		});
		return;
	};
	
};

class conFig {
	static async queryUser() {
		console.log('in Develpment');
		//ask on cl for username if none
		//ask if repeat user if set
		// const user = await Debug.askQuestion('Please login:\n"first.last":');
		// let userfolder = './users/'+ user
		// await fs.promises.mkdir(userfolder, { recursive: true })
		// return user;
	};
	static async loadProjects (user) {
		let proj = __dirname + '/users/'+user+'/projects.json'; verboselog(proj);
		let rawdata = fs.readFileSync(proj);
		let projects = JSON.parse(rawdata);
		return projects;
	};
	static async makeStream (path) {
		Debug.checkExists(path);
		let streams = [];
		path.forEach( function(item,index) {
			streams.push(fs.createWriteStream(item, {flags:'a'}))
		});
		return streams;
	};
};
class Report {
	static async genCsv(){

	};
};

class ampAdminpage{
	static async Login() {};


};

class ampWebpage {
	static async Login(url, page) {
		group('Login - AMP');
		try {
			await page.goto(url);
		} catch(ERR_ADDRESS_UNREACHABLE) {console.log('url error')};
		await page.type(LOCAL.amp.logincss, CREDS.username);
		await page.type(LOCAL.amp.pwcss, CREDS.password);
		await page.click(LOCAL.amp.loginbutton);
		await page.setViewport({ width: 1600, height: 900 });
		await page.waitFor(50);
		groupend('login - AMP');
		return page;
	};

	static async gotoPlanview(url, planarray, Upfile, Oldfile, Warnfile, page) {
		for (let view of planarray) {
			group('Planview ' + view);
			if (check) {let ans = await Debug.askQuestion("Check over Planview?\nNote:\n").then(Debug.print(ans))};
			await Debug.print(TEXT.loginmessage + view + '\nUrl:' + url + LOCAL.amp.planview + view, Upfile);
			await Debug.print(TEXT.loginmessage + view + '\nUrl:' + url + LOCAL.amp.planview + view, Warnfile);
			await Debug.print(TEXT.loginmessage + view + '\nUrl:' + url + LOCAL.amp.planview + view, Oldfile);
			await page.goto(url + LOCAL.amp.planview + view);
			for (let targetchild of TEXT.sensorarray) {
				await ampWebpage.getLastupdate(targetchild, Upfile, Oldfile, Warnfile, page)};
			groupend('Planview');
		};
		return page;
	};

	static async getLastupdate(targetchild, Upfile, Oldfile, Warnfile, page) {
		for (let typeofsensorbox of LOCAL.amp.label) {
			let namesel = 'body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + targetchild + LOCAL.amp.title;
			let valuesel = 'body > div:nth-child(' + typeofsensorbox + ') > div:nth-child(' + targetchild + LOCAL.amp.sensor;
				let name = await page.$(namesel);
				let link = await page.$(valuesel);
			try {
				const sensor =  await page.evaluate(name => name.textContent, name);
				const value =  await page.evaluate(link => link.textContent, link);
				const date = await page.evaluate(link => link.title, link);
				group('Sensor: ' + targetchild);
				let data = '\nSensor name: ' + sensor;
				data += '\nLast Updated on AMP: ';
				if (getvalue) {
					data += '\nCurrent value: ' + value;
				};
				const pdate = Date.parse(date);
				const pnowdate = Date.parse(TEXT.nowdate);
				const diff = Math.abs(pnowdate - pdate);
				if (diff < watchdog ) {
					data += date;
					if (verbose) {data += '\n' + TEXT.uptoDate};
					await Debug.print(data, Upfile);
				} else if (diff > watchdog & diff < watchlimit) {
					data += date;
					if (verbose) {data += '\n' + TEXT.behindDate};
					await Debug.print(data, Warnfile);
				} else {
					data += date;
					if (verbose) {data += '\n' + TEXT.oldDate};
					await Debug.print(data, Oldfile);
				};
				groupend('Sensor: ' + targetchild);
			}
			catch(error) {
				let exception = error.message.split(':');
				if (exception[0] = 'No node found for selector') {
				} else if (exception[0] = 'Evaluation failed') {
				} else if (exception[0] = 'UnhandledPromiseRejectionWarning') {
				} else {
					console.log('Caught:', error.message);
					await Debug.askQuestion('Will cont when ready')};
				}
		}
			return page;
	};
};

class qvWebpage {
	static async Login(page) {
		group('Login - QV');
		try {
			await page.goto(LOCAL.qv.urlstring)
		} catch (ERR_ADDRESS_UNREACHABLE) {
			console.log('url error')};
        await page.type(LOCAL.qv.logincss, CREDS.qvuser);
        await page.type(LOCAL.qv.pwcss, CREDS.qvpass);
        await page.click(LOCAL.qv.loginbutton);
		await page.setViewport({ width: 1600, height: 900 });
        await page.waitFor(2000);
        groupend('login - QV');
        return page;
    };

    static async gotoProject(page, namenum) {
		group('Project');
		await page.click(LOCAL.qv.menuprojects);
        await page.waitFor(200);
		await page.hover(LOCAL.qv.scrollbar);
        await page.waitFor(500);
		await page.click(LOCAL.qv.Qvprojectpre + namenum + LOCAL.qv.Qvprojectpost);
        await page.waitFor(500);
		groupend('Project');
		return page;
	};


	static async gotoView(planarray, Upfile, Warnfile, Oldfile, page) {
		for (let view of planarray) {
			group('Planview ' + view);
			await Debug.print(TEXT.loginmessage + view + '\n', Upfile);
			await Debug.print(TEXT.loginmessage + view + '\n', Warnfile);
			await Debug.print(TEXT.loginmessage + view + '\n', Oldfile);
			if (view != '0') {
				await page.click(LOCAL.qv.views);
        		await page.waitFor(500);
				await page.hover(LOCAL.qv.scrollbar2);
        		await page.waitFor(200);
				await page.click(LOCAL.qv.thumb+view);
			} else {};
			await page.waitFor(1000);
			for (let targetchild of TEXT.sensorarray) {
			    await qvWebpage.getLastupdate(targetchild, Upfile, Warnfile, Oldfile, page)};
			groupend('Planview' + view);
		};
		return page;
	};

    static async getLastupdate(targetchild, Upfile, Warnfile, Oldfile, page) {
		let sensor = '#objects > img:nth-child(' + targetchild + ')';
		try {
			await page.hover(sensor);
			group('Sensor: ' + sensor);
			const link = await page.$(LOCAL.qv.hoverbox);
			const txt =  await page.evaluate(link => link.innerHTML, link);
			let spltd = txt.split('<br>');
			let data = '\nSensor name: ' + spltd[0];
			let date = spltd[3].split("data: ").pop();
			// await Debug.print(data + ' \nDate:\n' + date + '\n', Upfile);
			const pdate = Date.parse(date);
			const pnowdate = Date.parse(TEXT.nowdate);
			const diff = Math.abs(pnowdate - pdate);
			if (diff < watchdog ) {
				data += date;
				if (verbose) {data += '\n' + TEXT.uptoDate};
				await Debug.print(data, Upfile);
			} else if (diff > watchdog & diff < watchlimit) {
				data += date;
				if (verbose) {data += '\n' + TEXT.behindDate};
				await Debug.print(data, Warnfile);
			} else {
				data += date;
				if (verbose) {data += '\n' + TEXT.oldDate};
				await Debug.print(data, Oldfile);
			};
			groupend('Sensor: ' + targetchild);
		}
		catch(UnhandledPromiseRejectionWarning) {};
		return;
	};
};

(async() => {
	if (preformance) {console.log(new Date().toISOString())};
	group('Main');
	const projects = await conFig.loadProjects(user);
	const parallelBatches = Math.ceil(projects.length / parallel);
	const browser = await puppeteer.launch(TEXT.head);
	let k = 0;
	for (let i = 0; i < projects.length; i += parallel) { k++;
		verboselog('\nBatch ' + k + ' of ' + parallelBatches);
		const promises = []
		for (let j = 0; j < parallel; j++) {
			let elem = i + j
			if (projects[elem] != undefined && projects[elem].skip != true) {
				let project = projects[elem].name;
				let planarray = projects[elem].planarray;
				let usercheckpath = __dirname + '\\users\\'+ CREDS.user + '\\dailychecks\\' + TEXT.filedate + '\\';
				await fs.promises.mkdir(usercheckpath, { recursive: true })
				let pathtofile = usercheckpath + '_all';
				let allpaths = [pathtofile+TEXT.outputfile,pathtofile+TEXT.pathtoOldfile,pathtofile+TEXT.pathtoWarnfile];
				let streams = await conFig.makeStream(allpaths);
				let Upfile = streams[0]; let Oldfile = streams[1]; let Warnfile = streams[2];
				const page = await browser.newPage();
				await Debug.print('Project:'+project+TEXT.scanplan+planarray+'\n'+TEXT.hasSitemessage + projects[elem].hassite + '\n', Upfile);
				await Debug.print('Project:'+project+TEXT.scanplan+planarray+'\n'+TEXT.hasSitemessage + projects[elem].hassite + '\n', Warnfile);
				await Debug.print('Project:'+project+TEXT.scanplan+planarray+'\n'+TEXT.hasSitemessage + projects[elem].hassite + '\n', Oldfile);
				promises.push(browser.newPage().then(
					async page => {
						if (projects[elem].hassite == 'amp') {
							if (preformance) {console.log(new Date().toISOString())};
							url = 'https://' + project + LOCAL.amp.urlstring;
							verboselog('Url: ' + url);
							const ampbuffer = await ampWebpage.Login(url, page);
							await Debug.print(TEXT.preloginmessage + project, Upfile);
							await Debug.print(TEXT.preloginmessage + project, Warnfile);
							await Debug.print(TEXT.preloginmessage + project, Oldfile);
							const ampnavigate = await ampWebpage.gotoPlanview(url, planarray, Upfile, Oldfile, Warnfile, ampbuffer);
							await ampnavigate.close();
							}
						else if (projects[elem].hassite == 'qv') {
							if (preformance) {console.log(new Date().toISOString())};
							let namenum = projects[elem].proj;
							const qvbuffer = await qvWebpage.Login(page);
							await Debug.print('\n' + TEXT.postloginmessage, Upfile);
							await Debug.print('\n' + TEXT.postloginmessage, Warnfile);
							await Debug.print('\n' + TEXT.postloginmessage, Oldfile);
							const qvproject = await qvWebpage.gotoProject(qvbuffer, namenum);
							await Debug.print('\nProject Switched to ' + project, Upfile);
							await Debug.print('\nProject Switched to ' + project, Warnfile);
							await Debug.print('\nProject Switched to ' + project, Oldfile);
							const qvscrape = await qvWebpage.gotoView(planarray, Upfile, Warnfile, Oldfile, qvproject);
							await qvscrape.close();
							}
						else if (projects[elem].hassite == 'truelook') {console.log('Truelook in develpment')};
						}));
			};
			await Promise.all(promises);
		};
	};
	await browser.close();
	groupend('Main');
	if (verbose) {group('exitmsg')};
	console.log('\n' + TEXT.exitmessage);
	if (verbose) {groupend('exitmsg')};
	if (preformance) {console.log(new Date().toISOString())};
})();
