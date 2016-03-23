import re
import json
from nltk.corpus import stopwords

TWEET_ID_LEN = 18

def dumpAfinn(file):
    afinnPath = open(file)
    afinn = {}
    for line in afinnPath:
        a = line.split('\t')
        afinn[a[0]] = int(a[1])
    return afinn

def trimWord(word):
    if word is '' or word.isdigit() or len(word) <= 2: return False
    return word.encode('UTF-8')
    
def splitTweet(string):
    try:
        obj = json.loads(string)
	nolinks = re.sub(r'http*[^ ]*', '', obj['text'], flags=re.MULTILINE).lower()
	return re.sub('[^0-9a-zA-Z\s]+', '', nolinks).split()
    except (KeyError,ValueError) as e:
        return False

def getStopwords():
	return stopwords.words('english') + stopwords.words('spanish') + stopwords.words('german') + stopwords.words('french') + stopwords.words('russian')
