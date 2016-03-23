#!/usr/bin/python
import os
import sys
import argparse
from export_topic_model import gatherTopicFiles
from generate_mallet_files import extract_tweets

def main(args):
    for root,dirs,files in os.walk(args.s):
        for file in files:
            keyword = os.path.splitext(file)[0]
            source_path = os.path.join(root,file)
            mallet_path = os.path.join(args.o,'mallet_files',keyword)
            tweet_mallet = os.path.join(mallet_path,'tweet.mallet')
            tweet_text = os.path.join(mallet_path,'tweet_text')
            tweet_doc = os.path.join(mallet_path,'tweet_doc')
            tweet_topics = os.path.join(mallet_path,'tweet_topics.txt')
            count = extract_tweets(source_path,mallet_path)
            num_topics = int(round(count/args.r,-1))
            if num_topics > 50: num_topics = 50
            elif num_topics <= 0: num_topics = 5
            os.system(
                'mallet import-dir --input {0} --output {1} --keep-sequence --remove-stopwords'.format(tweet_text,tweet_mallet)
            )
            os.system(
                'mallet train-topics --input {0} --num-topics {3} --num-iterations 1000 --optimize-interval 10 --output-doc-topics {1} --output-topic-keys {2} --num-threads 4'.format(tweet_mallet,tweet_doc,tweet_topics,num_topics)
            )
            gatherTopicFiles(os.path.join(args.o,'mallet_files'),args.o,args.f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create the topic models for tweets')
    parser.add_argument('-s', type=str, help='source directory of where to find raw tweets', required=True)
    parser.add_argument('-o', type=str, help='output directory of where to put the "topic_models" file', required=True)
    parser.add_argument('-r', type=str, help='tweets per topic', default=50)
    parser.add_argument('-f', type=str, help='file format (csv or json)',required=True)
    parser.add_argument('-w', type=str, help='wipe mallet files')
    args = parser.parse_args()
    main(args)
