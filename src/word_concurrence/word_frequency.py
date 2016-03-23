#!/bin/python

import sys
import os
import argparse
import json
import re
from collections import OrderedDict
from word_processor import *
from utility import byteify

def main(args):
	obj = {}
	sw = getStopwords()
	for root, dirs, files in os.walk(args.dir):
		for file in files:
			fpath = os.path.join(root,file)
			tag = os.path.splitext(file)[0]
			obj[tag] = get_score(fpath ,dumpAfinn(args.afinn),sw)
	if args.fileFormat == 'json':
		exportJSON(args.output,obj)
	elif args.fileFormat == 'csv':
		exportCSV(args.output,obj)

def get_score(file,afinn,sw):
	scoresPath = open(file)
	scores = {}
	print 'Processing {0}...\n'.format(file)
	for string in scoresPath:
		for line in re.sub(r'}{', '}\n{', string, flags=re.MULTILINE).split('\n'):
			words = splitTweet(line)
			if not words: continue
			for str in words:
				word = trimWord(str)
				if word is False or word in sw:
					continue
				if not scores.get(word,False):
					scores[word] = {"count":0,"sentiment":0}
				sentiment = afinn.get(word,False)
				if sentiment is not False:
					scores[word]["sentiment"] += int(sentiment)
				scores[word]["count"] += 1
	scoresPath.close()
	return scores

def exportJSON(outPath,data):
	with open(outPath,'w+') as o:
		o.write(json.dumps(data))

def exportCSV(outPath,data):
	freq = byteify(data)
	with open(outPath,'w+') as o:
		o.write('tag,word,count,sentiment\n')
		for tag in freq:
			for word in freq[tag]:
				count = str(freq[tag][word]['count'])
				sentiment = str(freq[tag][word]['sentiment'])
				o.write(tag+','+word+','+count+','+sentiment+'\n')
				
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Find word frequency of words in each json file')
	parser.add_argument('-d', help='directory to look for jsons', dest='dir', required=True)
	parser.add_argument('-o', help='output file', dest='output', required=True)
	parser.add_argument('-a', help='afinn file', dest='afinn', required=True)
	parser.add_argument('-f', help='file format (csv or json)', dest='fileFormat', required=True)
	args = parser.parse_args()
	main(args)
