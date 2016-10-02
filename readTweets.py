import re
import sys
from nltk.tokenize import word_tokenize
import codecs


 
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
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


if __name__ == "__main__":
  reload(sys)
  sys.setdefaultencoding('utf8')
  # for elem in read_tweets("prueba.txt"):
  #   print elem[1].encode('utf-8')
  tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE | re.UNICODE )
  emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE | re.UNICODE)
  
  tweets = read_tweets("tweets.txt")
  for tweet in tweets:
    tweet['tokens'] = preprocess(tweet['text'])
    # print(tweet['tokens'])
    for token in tweet['tokens']:
      print("token "+ token.encode('utf-8'))

