# -*- coding: utf-8 -*-
import re
import random
import csv
import sys
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import codecs
from nltk.util import ngrams
from nltk import bigrams
import nltk
from nltk.collocations import *
from operator import itemgetter
from readWekaRes import read_weka_res


from nltk.corpus import cess_esp as cess
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt

from nltk.tag import StanfordNERTagger
 
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
    tokens = word_tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def dump_csv(tweets):
  with open('data.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=':',)
    for tweet in tweets:
      spamwriter.writerow([tweet.owner, tweet.date, tweet.text, tweet.retweets, tweet.tokens])

def freqCount(ngram, tweets):
  freq_list = []
  for gram in ngram:
    c = 0
    sentence = ""
    n = len(gram)
    for word in gram:
      sentence += (word + " ") if (n != 1) else word
      n -= 1
    for tweet in tweets:
      if sentence in tweet['text']:
        c += 1
    freq_list.append((gram,c))
  return freq_list

def ngramFreq(ngram):
  return ngram[1]

if __name__ == "__main__":
  reload(sys)
  sys.setdefaultencoding('utf8')
  # for elem in read_tweets("prueba.txt"):
  #   print elem[1].encode('utf-8')
  tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE | re.UNICODE )
  emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE | re.UNICODE)
  
  #Paths for the ner tagger
  PATH_TO_MODEL = "/home/francisco/Downloads/stanford-ner-2015-04-20/classifiers/spanish.ancora.distsim.s512.crf.ser.gz"
  PATH_TO_JAR = "/home/francisco/Downloads/stanford-ner-2015-04-20/stanford-ner.jar"
  
  tagger = StanfordNERTagger(model_filename=PATH_TO_MODEL, path_to_jar=PATH_TO_JAR)
  
  tweets = read_tweets("tweets.txt")
  with open('tweets.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar="'", quoting=csv.QUOTE_ALL)

    all_tokens = []
    all_tokens_wstops = []
    for tweet in tweets:
      
      tweet['text'] = re.sub(r'(?:(?:\d+,?)+(?:\.?\d+)?)', "",tweet['text'])
      tweet['text'] = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', "", tweet['text'])
      tweet['text'] = re.sub(r"\n",' ',tweet['text'])
      tweet['text'] = re.sub(r"\.",' ',tweet['text'])
      tweet['text'] = re.sub(r"-",' ',tweet['text'])
      tweet['text'] = re.sub(r":",' ',tweet['text'])
      tweet['text'] = re.sub(r";",' ',tweet['text'])
      tweet['text'] = re.sub(r'\&',' ',tweet['text'])
      tweet['text'] = re.sub(r"\"", '\'', tweet['text'])
      tweet['text'] = re.sub(r',',' ',tweet['text'])
      tweet['text'] = re.sub(r'\[',' ',tweet['text'])
      tweet['text'] = re.sub(r'\]',' ',tweet['text'])
      tweet['text'] = re.sub(r"'",' ',tweet['text'])
      tweet['text'] = re.sub(r"\(",' ',tweet['text'])
      tweet['text'] = re.sub(r"\)",' ',tweet['text'])
      tweet['text'] = re.sub(r"\'\'",' ',tweet['text'])
      tweet['text'] = re.sub(r"`",' ',tweet['text'])
      tweet['text'] = re.sub(r"_",' ',tweet['text']) 
      tweet['text'] = re.sub(r"\?",' ',tweet['text'])
      tweet['text'] = re.sub(r"¿",' ',tweet['text'])
      tweet['text'] = re.sub(r"!",' ',tweet['text'])
      tweet['text'] = re.sub(r"¡",' ',tweet['text'])
      tweet['text'] = re.sub(r"\"",' ',tweet['text'])
      tweet['text'] = re.sub(r"‘",' ',tweet['text'])
      tweet['text'] = re.sub(r"\.",' ',tweet['text'])
      tweet['text'] = re.sub(r"/",' ',tweet['text'])
      
      tweet['text'] = re.sub(r"\.\.\.",' ',tweet['text'])      
      tweet['text'] = re.sub(r"\+",' ',tweet['text'])
      tweet['text'] = re.sub(r"\$",' ',tweet['text'])
      tweet['text'] = re.sub(r"%",' ',tweet['text'])
      tweet['text'] = re.sub(r"\|",' ',tweet['text'])
      tweet['text'] = re.sub(r"@\w*",' ',tweet['text'])

      #Write csv   
      # if random.random() > 0.5:
      #   spamwriter.writerow([tweet['text'],"yes"])
      # else:
      #   spamwriter.writerow([tweet['text'],"no"])
      # print tweet['text']

      #Text clean up 
      # tweet['text'] = re.sub(r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", "", tweet['text'])
      
      # tweet['text'] = tweet['text'].lower()
      #Tokenization
      # tweet['tokens'] = preprocess(tweet['text'])
      # print tweet['tokens']
      # #Tagging
      # tweet['tags'] = tagger.tag(tweet['tokens'])
      # print tweet['tags']
      # all_tokens_wstops  = all_tokens_wstops + tweet['tokens']
      # important_words=[]
      # for token in tweet['tokens']:
      #   if token not in stopwords.words('spanish'):
      #       important_words.append(token)

      # tweet['tokens'] = important_words
      # all_tokens = all_tokens + tweet['tokens']

# Gram calculation
# unigrams = list(ngrams(all_tokens,1))
# bigrams = list(ngrams(all_tokens,2))
# trigrams = list(ngrams(all_tokens_wstops,3))
# for gram in bigrams:
#   print gram

# Gram freq Calculation
# freq = freqCount(unigrams,tweets)
# freq2 = freqCount(bigrams,tweets)
# freq3 = freqCount(trigrams,tweets)

#Gram sorting
# ordered_grams = sorted(set(freq), key=ngramFreq)[::-1]
# print "UNIGRAM(300):\n"
# i = 1
# for item in ordered_grams[:300]:
#   #print str(i)+":",item
#   i = i + 1 

# ordered_grams = sorted(set(freq2), key=ngramFreq)[::-1]
# print "BIGRAM(150):\n"
# i = 1
# for item in ordered_grams[:150]:
#   #print str(i)+":",item
#   i = i + 1 

# ordered_grams = sorted(set(freq3), key=ngramFreq)[::-1]
# print "TRIGRAM(150)\n"
# i = 1
# for item in ordered_grams[:150]:
#   #print str(i)+":",item
#   i = i + 1 
 

# PMI calculius 
# trigram_measures = nltk.collocations.TrigramAssocMeasures()
# finder = TrigramCollocationFinder.from_words(all_tokens)
# tri=finder.score_ngrams(trigram_measures.pmi)
# finder = BigramCollocationFinder.from_words(all_tokens)
# Bi=finder.score_ngrams(trigram_measures.pmi)
# Bi = [k for k in Bi if k[1]>9]
# tri = [k for k in tri if k[1]>9]

# TOT=tri+Bi
# TOT=sorted(TOT,key=itemgetter(1),reverse=True)
# for i in range(len(TOT)):
#     print TOT[i][0][0],TOT[i][0][1],TOT[i][1] 

what = read_weka_res('list_trigram_bigram_what.arff') + read_weka_res('list_unigram_what.arff')
when = read_weka_res('list_trigram_bigram_when.arff') + read_weka_res('list_unigram_when.arff')
how = read_weka_res('list_trigram_bigram_how.arff') + read_weka_res('list_unigram_how.arff')

num_yes = 0
num_no = 0
# Esto clasifica los tweets en base a las palabras obtenidas con la herramienta de WEKA.
for tweet in tweets: 
  yes = False
  for w in what:
    if w in tweet['text']:
      yes = True
      break
  for w in how:
    if w in tweet['text']:
      yes = True
      break
  if yes:
    tweet['crime'] = 'yes'
    num_yes += 1
  else:
    tweet['crime'] = 'no'
    num_no += 1

print "% de yes: ", (num_yes/float(len(tweets)))*100
print "% de no: ", (num_no/float(len(tweets)))*100