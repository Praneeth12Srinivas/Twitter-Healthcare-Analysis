from pymongo import MongoClient
import os
import sys
import json
import shutil
import argparse
import codecs
from datetime import date
from utility import *

def main(args):
    host = args.host
    port = args.port
    database = args.database
    collection = args.collection
    DATA_DIRECTORY = args.datasource
    ARCHIVE_DIRECTORY = args.archive

    client = MongoClient(host=host, port=port)
    db = client[database]
    coll = db[collection]

    document_count = 0
    skipped_count = 0
    json_files = get_all_files(os.path.abspath(DATA_DIRECTORY), 'json')
    for json_file in json_files:
        if json_file == date.today().strftime('%Y-%m-%d'):
            continue
        print 'Loading {0}'.format(json_file)
        with codecs.open(json_file,encoding="utf-8") as f:
            for line in f:
                try:
                    if not line.isspace():
                        json_data = json.loads(line)
                        coll.insert_one(json_data)
                        document_count += 1
                except ValueError as e:
                    skipped_count += 1
                    print 'Skipping Bad JSON Record ({0}):'.format(skipped_count), e
                    continue
        print '{0} bad records skipped in total'.format(skipped_count)
        f.close()
    print '{0} records added to MongoDB'.format(document_count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import data into a MongoDB collection')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=27017)
    parser.add_argument('--database', type=str,required=True)
    parser.add_argument('--collection', type=str,required=True)
    parser.add_argument('--datasource', type=str,required=True)
    parser.add_argument('--archive', type=str,required=True)
    args = parser.parse_args()
    main(args)
