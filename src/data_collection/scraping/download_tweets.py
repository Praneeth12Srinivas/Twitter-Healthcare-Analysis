from __future__ import print_function
from auth_manager import AuthManager
import sys
import os
import jsonpickle
import tweepy
import argparse

class TweetsCollector:
    def __init__(self,input,output,auth_manager):
		self.api = tweepy.API(auth_manager.auth_handlers[0],wait_on_rate_limit=True)
		if not os.path.exists(output):
			os.makedirs(output)
		for root, dirs, files in os.walk(input):
			for f in files:                 
				if os.path.splitext(f.lower())[1] == '.json':
					self.tag = os.path.splitext(f.lower())[0]
					self.file = os.path.join(output,f)
					self.collectTweets(os.path.join(input,f))

    def collectTweets(self,file):
		with open(file, 'r') as f:
			arrayList = list(set(f.read().split(',')))
			count = 0
			print("{0}: Searching tweets...".format(self.tag))
			with open(self.file, 'w+') as o:
				for ids in chunk(arrayList,100):
					print("{0}: Collecting {1} of {2} tweets...\r\r".format(self.tag, count,len(arrayList)))
					try:
						new_tweets = self.api.statuses_lookup(ids)
						for tweet in new_tweets:
							o.write(jsonpickle.encode(tweet._json, unpicklable=False)+'\n')
						count += len(new_tweets)
					except tweepy.TweepError as e:
						print("Err: " + str(e))
				print ("{0}: Downloaded {1} tweets".format(self.tag,count))
		
			
def chunk(l,n):
	for i in xrange(0, len(l), n):
		yield l[i:i+n]
		
def main(args):
	CREDENTIALS_FILE_PATH = os.path.join(args.c)
	auth_manager = AuthManager(CREDENTIALS_FILE_PATH)
	TweetsCollector(args.i,args.o,auth_manager)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Import data into a MongoDB collection')
	parser.add_argument('-i', type=str, required=True, help="Folders consisiting of files each containing a comma-separated list of tweet IDs")
	parser.add_argument('-c', type=str, required=True, help="Credentials file in JSON")
	parser.add_argument('-o', type=str, required=True, help="Output directory")
	args = parser.parse_args()
	main(args)