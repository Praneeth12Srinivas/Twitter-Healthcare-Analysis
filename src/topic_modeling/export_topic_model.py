#!/bin/python

import sys
import os
import argparse
import json

def gatherTopicFiles(dir,output,fileFormat):
    obj = {}
    for root, dirs, files in os.walk(dir):
        if files == [] or 'tweet_topics.txt' not in files: continue
        tag = os.path.basename(root)
        topicsPath = os.path.join(root,'tweet_topics.txt')
        obj[tag] = []
        with open(topicsPath) as f:
            for line in f:
                try:
                    obj[tag].append(line.strip().split('\t')[2])
                except IndexError:
                    continue
    
    if fileFormat == 'csv':
        exportCSV(os.path.join(output),obj)
    elif fileFormat == 'json':
        exportJSON(os.path.join(output),obj)
    else:
        print 'Please specify a file format'
                    
def exportJSON(outPath,data):
    with open(outPath,'w+') as o:
        o.write(json.dumps(data))

def exportCSV(outPath,data):
    with open(outPath,'w+') as o:
        o.write('tag,topics\n')
        for tag in data:
            o.write(tag+',"'+','.join(data[tag])+'"\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gather all topics for each tag')
    parser.add_argument('-d', help='directory to look for tweet_topics.txt', dest='dir', required=True)
    parser.add_argument('-o', help='output file', dest='output', required=True)
    parser.add_argument('-f', help='file format (json or csv)', dest='fileFormat', required=True)
    args = parser.parse_args()
    gatherTopicFiles(args.dir,args.output,args.fileFormat)
