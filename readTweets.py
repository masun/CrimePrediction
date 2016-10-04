# -*- coding: utf-8 -*-
import re
import csv
import sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import codecs
from nltk.util import ngrams


 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:\w[a-z'\-_]+\w)", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

def parseString(string):
  newString = ""
  for char in string:
    if (char == u"Á"):
      newString += "A"
    elif (char == u"á"):
      newString += "a"
    elif (char == u"É"):
      newString += "E"
    elif (char == u"é"):
      newString += "e"
    elif (char == u"Í"):
      newString += "I"
    elif (char == u"í"):
      newString += "i"
    elif (char == u"Ó"):
      newString += "O"
    elif (char == u"ó"):
      newString += "o"
    elif (char == u"Ú"):
      newString += "U"
    elif (char == u"ú"):
      newString += "u"
    elif (char == u"Ñ"):
      newString += "N"
    elif (char == u"ñ"):
      newString += "n"
    else:
      newString += char
  return newString
    
def read_tweets(name):
  try:
    # f = open(name, 'r') 
    f = codecs.open(name, encoding='utf-8')
    data = f.readlines()
    account = ""
    tweets = []
    for line in data:
      if (line[0] != "["):
        account = line[:-1] # Removing "\n"
        account = account[:-1] # Removing ":"
      else:
        info = line.split("][")
        info.append(account)
        info[0] = info[0][1:] # Removing "["
        info[1] = info[1].decode("utf-8")
        info[2] = info[2][:-1] # Removing "\n"
        info[2] = info[2][:-1] # Removing "]"
        # info[1] = parseString(info[1])
        elem = {
          'owner':account,
          'date':info[0],
          'text':info[1],
          'retweets':info[2]
        }
        tweets.append(elem)
    f.close()
    return tweets
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    sys.exit(1)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = word_tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def dump_csv(tweets):
  with open('data.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=':',)
    for tweet in tweets:
      spamwriter.writerow([tweet.owner, tweet.date, tweet.text, tweet.retweets, tweet.tokens])

if __name__ == "__main__":
  reload(sys)
  sys.setdefaultencoding('utf8')
  # for elem in read_tweets("prueba.txt"):
  #   print elem[1].encode('utf-8')
  tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE | re.UNICODE )
  emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE | re.UNICODE)
  
  tweets = read_tweets("tweets.txt")
  all_tokens = []
  for tweet in tweets:
    tweet['tokens'] = preprocess(tweet['text'])
    important_words=[]
    for token in tweet['tokens']:
      if token not in stopwords.words('spanish'):
          important_words.append(token)

    tweet['tokens'] = important_words
    all_tokens.append(tweet['tokens'])

    # print stopwords.words('spanish')
    for token in tweet['tokens']:
      print("token "+ token.encode('utf-8'))
    # print tweet['date'] 
    # print tweet['text'] 
    # print tweet['tokens'] 

  # bigrams = ngrams(all_tokens,2)
  # for gram in bigrams:
  #   print gram