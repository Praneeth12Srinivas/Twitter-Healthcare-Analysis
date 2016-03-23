#!/bin/python

import sys
import os
import argparse

def main(args):
    obj = {}
    for root,dirs,files in os.walk(args.d):
        for file in files:
            fObj = os.path.splitext(file)
            if fObj[1] == '.json':
                with open(os.path.join(root,file)) as f:
                    obj[fObj[0]] = len(f.readlines())
    if args.f == 'csv':
        exportCSV(args.o,obj)
    elif args.f == 'json':
        exportJSON(args.o,obj)
    
def exportJSON(outPath,data):
    with open(outPath,'w+') as o:
        o.write(json.dumps(data))

def exportCSV(outPath,data):
    with open(outPath,'w+') as o:
        o.write('tag,count\n')
        for tag in data:
            o.write(tag+','+str(data[tag])+'\n')
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find top tags based on number of tweets')
    parser.add_argument('-d', help='directory to look for json', required=True)
    parser.add_argument('-o', help='output file', required=True)
    parser.add_argument('-f', help='file format (csv or json)', required=True)
    args = parser.parse_args()
    main(args)
