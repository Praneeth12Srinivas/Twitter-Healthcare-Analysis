#!/bin/python

import sys
import os
import argparse
import json

def main(args):
	obj = {}
	for root, dirs, files in os.walk(args.dir):
		if files == []: continue
		tag = os.path.splitext(filter(lambda f: 'json' in f, files)[0])[0]
		topicsPath = os.path.join(root,'topic_keys.txt')
		with open(topicsPath) as f:
			for line in f:
				try:
					obj[tag] = line.strip().split('\t')[2].split(' ')
				except IndexError:
					continue
	with open(args.output,'w+') as out:
		if args.fileFormat == 'json':
			out.write(json.dumps(obj))
		elif args.fileFormat == 'csv':
			out.write('tag,topics\n')
			for tag in obj:
				if obj[tag] != '':
					out.write(tag+',"'+','.join(obj[tag])+'"\n')
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Gather all topics for each tag')
	parser.add_argument('-d', help='directory to look for topics_keys.txt', dest='dir', required=True)
	parser.add_argument('-o', help='output file', dest='output', required=True)
	parser.add_argument('-f', help='file format (json or csv)', dest='fileFormat', required=True)
	args = parser.parse_args()
	main(args)
