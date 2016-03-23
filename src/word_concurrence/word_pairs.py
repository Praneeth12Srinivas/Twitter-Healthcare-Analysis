#!/bin/python

import sys
import os
import argparse
import json
import re
from collections import OrderedDict
from word_processor import *

def main(args):
    allWordPairs = {}
    sw = getStopwords()
    for root, dirs, files in os.walk(args.dir):
        for file in files:
            tag = os.path.splitext(file)[0]
            print 'Processing {0}...'.format(tag)
            allWordPairs[tag] = processTweets(os.path.join(root,file),sw)
    if args.fileFormat == 'json':
        exportJSON(args.output,allWordPairs)
    elif args.fileFormat == 'csv':
        exportCSV(args.output,allWordPairs)

def processTweets(tweetsPath,sw):
    wordPairs = {}
    with open(tweetsPath) as tweets:
        for string in tweets:
            lines = re.sub(r'}{', '}\n{', string, flags=re.MULTILINE).split('\n')
            if lines is False or lines is []:
                continue
            for line in lines:
                words = splitTweet(line)
                if words is False: continue
                for word in words:
                    makePairs(wordPairs,words,trimWord(word,sw),sw)
        return wordPairs
    
def makePairs(pairs, words, newWord, sw):
    lineKeys = []
    for word in words:
        word = trimWord(word,sw)
        if not word or not newWord or word == newWord: continue
        sortedKey = sorted([newWord,word])
        pairKey = '-'.join(sortedKey)
        try:
            if pairKey not in lineKeys:
                pairs[pairKey][0] += words.count(sortedKey[0])
                pairs[pairKey][1] += words.count(sortedKey[1])
                pairs[pairKey][2] += 1
        except KeyError:
            lineKeys.append(pairKey)
            pairs[pairKey] = [0,0,0]
    
def exportJSON(outPath,data):
    with open(outPath,'w+') as o:
        o.write(json.dumps(data))

def exportCSV(outPath,concurrence):
    with open(outPath,'w+') as o:
        o.write('tag,word1,word2,concurrence_count,word1_occurance,word2_occurance\n')
        for tag in concurrence:
            for pair in concurrence[tag]:
                words = pair.split('-')
                word1 = '"'+words[0]+'"'
                word2 = '"'+words[1]+'"'
                word1_count = concurrence[tag][pair][0]
                word2_count = concurrence[tag][pair][1]
                concurrence_count = concurrence[tag][pair][2]
                o.write(tag+','+word1+','+word2+','+str(concurrence_count)+','+str(word1_count)+','+str(word2_count)+'\n')
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find word pairs in each tweet')
    parser.add_argument('-d', help='directory to look for jsons', dest='dir', required=True)
    parser.add_argument('-o', help='output file', dest='output', required=True)
    parser.add_argument('-f', help='file format (csv or json)', dest='fileFormat', required=True)
    args = parser.parse_args()
    main(args)
