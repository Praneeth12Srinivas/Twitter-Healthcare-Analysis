#!/usr/bin/python
import sys
import json
import codecs
import re
import os
import time
import sys
import re
import argparse

def extract_tweets(file_name,output_dir):
    t0 = time.time()
    print 'Generating mallet files for '+file_name+'...'
    output_path = os.path.join(output_dir,"tweet_text")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_big_file = 'all_tweets.txt'
    bigflattext = open(os.path.join(output_path,output_big_file),'w')
    count = 0
    bad_count = 0
    with codecs.open(file_name,encoding="utf-8") as f1:
        for line in f1:
            try:
                count += 1
                data = json.loads(line)
                result = output_path + '/tweet_' + str(data['id']) + '.txt'
                out = re.compile(r'\W*\b\w{1,3}\b').sub('', data['text'].encode('ascii','ignore').translate(None,'\n'))
                noHyperLink = re.sub(r'/http.* /g', '', out)
                json.dump(noHyperLink, open(result, 'w'))
                bigflattext.write(str(data['id']) + ' '*5 + noHyperLink + '\n' )
            except ValueError:
                print 'Bad JSON record, skipping...', bad_count
                bad_count += 1
            continue
    bigflattext.close()
    print 'Finished. Took {0:4.1f} minutes.'.format((time.time()-t0)/60.)
    print '{0} / {1} tweets successfully extracted.'.format(count,count+bad_count)
    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create folder structure for analysis in mallet')
    parser.add_argument('-f', type=str, help='file', required=True)
    parser.add_argument('-o', type=str, help='output directory', required=True)
    args = parser.parse_args()
    extract_tweets(args.f,args.o)
