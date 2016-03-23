#!/bin/python
import sys
import os
import argparse
import json
from utility import *


reload(sys)
sys.setdefaultencoding('utf-8')

def main(args):
    obj = {}
    for root,dirs,files in os.walk(args.d):
        for file in files:
            fObj = os.path.splitext(file)
            tag = fObj[0]
            ext = fObj[1]
            if ext == '.json':
                obj[tag] = {}
                with open(os.path.join(root,file)) as f:
                    for line in f:
                        fields = getFieldsFromJSON(line,['id_str','user.screen_name','user.description','user.followers_count','user.profile_background_image_url'],True)
                        if fields['screen_name'] in obj[tag]:
                            obj[tag][fields['screen_name']]['count'] += 1
                            obj[tag][fields['screen_name']]['tweets'].append(fields['id_str'])
                        else:
                            obj[tag][fields['screen_name']] = {
                                'tweets': [fields['id_str']],
                                'description': fields['description'],
                                'followers': fields['followers_count'],
                                'icon': fields['profile_background_image_url'],
                                'count': 1
                            }
    for tag in obj:
        obj[tag] = runQuery(obj[tag],args.s,args.l)[:int(args.l)]
    if args.f == 'csv':
        exportCSV(args.o,obj)
    elif args.f == 'json':
        exportJSON(args.o,obj)
    
def runQuery(dict,sortBy='count',limit=15):
    list = []
    for username in dict:
        dict[username]['screen_name'] = username
        list.append(dict[username])
    return sorted(list, key=lambda x: x[sortBy], reverse=True)
    
def exportJSON(outPath,data):
    with open(outPath,'w+') as o:
        o.write(json.loads(data))

def exportCSV(outPath,data):
    with open(outPath,'w+') as o:
        o.write('tag,count,screen_name,description,followers,tweets,icon\n')
        for tag in data:
            for user in data[tag]:
                o.write(tag+','+str(user['count'])+','+user['screen_name']+',"'+user['description'].replace('\r','').replace('\n','')+'",'+str(user['followers'])+',"'+','.join(user['tweets'])+'",'+user['icon']+'\n')
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find top users based on either followers count or tweets count')
    parser.add_argument('-d', help='directory to look for id lists', required=True)
    parser.add_argument('-o', help='output file', required=True)
    parser.add_argument('-f', help='file format (csv or json)', required=True)
    parser.add_argument('-l', help='limit', default=50)
    parser.add_argument('-s', help='sort by ("followers" or "count")', default="count")
    args = parser.parse_args()
    main(args)
