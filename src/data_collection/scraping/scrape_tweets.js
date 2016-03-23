/*************************************************************************
	scrape.tweets.js

	Author:
		Wai Yin Wong (Falcon)
		
	Description:
		This program gathers tweet ids in a comma delimited file
		
	Usage:
		$ node scrape-tweets.js -t ["filename"] -o ["dirname"] [-c]
		-t [tagsFile]: file of one keyword per line
		-o [outputDirectory]: where scraped data will be saved
		-c: creates directory if it does not already exist
	
*************************************************************************/ 

const request = require('request');
const fs = require('fs');
const yargs = require('yargs').argv;
const path = require('path');
const url = 'https://twitter.com/search';

Array.prototype.clean = function(deleteValue) {for (var i = 0; i < this.length; i++) {if (this[i] == deleteValue) {this.splice(i, 1);i--;}}return this;};
Math.randomRange = function(a,b) { return a + Math.random()*(b-a); };

function Scrapper () {
	this.ui = new Interface(this);
	this.tags = {};
	this.allTweets = [];
	if (yargs.h) this.ui.getHelp();
	else this.ui.searchTags(
		this.ui.getTags(),
		this.ui.getOutputDirectory()
	);
}

Scrapper.prototype = {
	log: function (string,filename) {
		fs.writeFile(path.join(yargs.o,(filename?filename:'debug.txt')), JSON.stringify(string), { flag: 'w+' }, function(err) {});
	}
};

function Interface (p) {
	this.parent = p;
};
Interface.prototype = {
	getHelp: function () {
		console.log(
			'$ node scrape-tweets.js -t ["filename"] -o ["dirname"] [-c]\n'+
			'-t [tagsFile]: file of one keyword per line\n'+
			'-o [outputDirectory]: where scraped data will be saved\n'+
			'-c: creates directory if it does not already exist'
		);
	},
	getTags: function () {
		if (typeof yargs.t == 'string')
			return fs.readFileSync(yargs.t, 'utf8').split('\r\n').clean('');
		else
			console.log('option -t [tagsFile] is required');
	},
	getOutputDirectory: function () {
		if (typeof yargs.o == 'string')
			return yargs.o;
		else
			console.log('option -o [outputDirectory] is required');
	},
	searchTags: function (tags, dir) {
		if (!dir || !tags) return;
		if (!fs.existsSync(dir) && yargs.c)
			fs.mkdirSync(dir);
		for (var i = 0; i < tags.length; i++)
			this.recordData({
				tag:tags[i],
				path:path.join(dir,tags[i]+'.json'),
				url:'https://twitter.com/search?q='+tags[i],
				type:'search'
			});
	},
	recordData: function (o) { var self = this;
		var req = request(o.url, function (error, response, body) {
			if (!error && response.statusCode == 200) {
				if (!self.parent.tags[o.tag])
				self.parent.tags[o.tag] = {
					tweetIDs:[],
					max_position: false,
					last_note_ts: false
				};
				var data = self.parseData(body,o.tag,o.type);
				if (!data) { console.log(tweetCount+' tweets collected for "'+o.tag+'"'); return; }
				fs.writeFile(o.path, data.tweets, { flag: 'a+' }, function(err) {
					if (err) throw err;
					setTimeout(function(){
						self.recordData({
							tag:o.tag,
							path:o.path,
							url:data.url,
							type:'scroll'
						});
					}, Math.randomRange(500,1200).toFixed(0));
				});
				var tweetCount = self.parent.tags[o.tag].tweetIDs.length;
				console.log('Data('+tweetCount+') from "'+o.tag+'" received!');
			}
		});
	},
	parseData: function (data,tag,type) {
		var tweets = [];
		if (type == 'scroll') {
			tweets = JSON.parse(data).items_html.match(/id="stream-item-tweet-(.*?)"/g);
		} else if (type == 'search') {
			tweets = data.match(/id="stream-item-tweet-(.*?)"/g);
		}
		if (!tweets) return;
		for (var i=0;i<tweets.length;i++)
			this.parent.tags[tag].tweetIDs.push(tweets[i].match(/\d+/)[0]);
		var url = type == 'search' ?
				this.searchURL(data,tag,this.parent.tags[tag].tweetIDs[-1]) :
				this.scrollURL(data,tag);
		return {
			tweets: this.parent.tags[tag].tweetIDs,
			url: url
		};
	},
	scrollURL: function (string,tag) {
		var position_string = string.match(/"min_position":"(.*?)"/)[1].split('-');
			position_string[1] = this.parent.tags[tag].tweetIDs.slice(-1)[0];
		this.parent.tags[tag].max_position = position_string.join('-');
		return this.getURL(tag);
	},
	searchURL: function (string,tag) {
		this.parent.tags[tag].max_position = string.match(/data-max-position="(.*?)"/)[1];
		this.parent.tags[tag].last_note_ts = string.match(/data-time="(.*?)"/)[1];
		return this.getURL(tag);
	},
	getURL: function (tag) {
		var url = 'https://twitter.com/i/search/timeline?';
		return url+[
			'vertical=default',
			'include_available_features=1',
			'include_entities=1',
			'q='+tag,
			'max_position='+this.parent.tags[tag].max_position,
			'last_note_ts='+this.parent.tags[tag].last_note_ts,
			'reset_error_state=false'
		].join('&');
	}
};
new Scrapper();
