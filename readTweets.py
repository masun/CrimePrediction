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
from datetime import datetime
import dateutil.relativedelta

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
        info[0] = datetime.strptime(info[0], '%Y-%m-%d %H:%M:%S')
        info[1] = info[1].decode("utf-8")
        info[2] = info[1][:-1] # Removing "\n"
        info[2] = info[1][:-1] # Removing "]"
        elem = {
          'owner':account,
          'date':info[0],
          'text':info[1]
        }
        tweets.append(elem)
    f.close()
    return sorted(tweets, key=lambda x: x['date'])
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
  
  what = [
  "secuestro",
  "secuestrar",
  "secuestraron",
  "asesinar",
  "asesino",
  "asesinaron",
  "asesinó",
  "violación",
  "violaron",
  "robo",
  "robaron",
  "secuestró",
  "asesinato",
  "extorsión",
  "violación",
  "violaron",
  "mataron",
  "mató"]

  when = [
  "madrugada",
  "noche",
  "día",
  "mañana",
  "tarde",
  "mediodía",
  "anoche"
  ]

  how = [
  "quemado",
  "quemaron",
  "quemo",
  "armados",
  "golpes",
  "golpe",
  "golpearon",
  "golpeó",
  "droga",
  "drogas",
  "bombas",
  "tiro",
  "tiros",
  "tiroteado",
  "tiroteados",
  "tirotearon",
  "tiroteo",
  "revolver",
  "puñaladas",
  "puñaladas",
  "pistola",
  "pistolas",
  "plomo",
  "lacrimógenas",
  "lacrimógena",
  "escopeta",
  "escopetas",
  "dispara",
  "disparan",
  "disparando",
  "disparó",
  "dispararon",
  "disparos",
  "cuchillo",
  "cocaína",
  "bomba",
  "bala",
  "balas",
  "armamento",
  "armado",
  "armas",
  "tiroteo",
  "fusil",
  "cuchillo",
  "cuchillos",
  "disparo",
  "fusiles",
  "granada",
  "navaja",
  "ametralladora",
  "bisturí",
  "proyectil",
  "arma blanca",
  "arma de fuego",
  "acuchillado",
  "explosión",
  "cuchilladas",
  "armados",
  "gasolina",
  "incendio"
  ]

  what += read_weka_res('gram_lists/list_trigram_bigram_what.arff') + read_weka_res('gram_lists/list_unigram_what.arff')
  when += read_weka_res('gram_lists/list_trigram_bigram_when.arff') + read_weka_res('gram_lists/list_unigram_when.arff')
  how += read_weka_res('gram_lists/list_trigram_bigram_how.arff') + read_weka_res('gram_lists/list_unigram_how.arff')
  where = read_weka_res('gram_lists/list_trigram_bigram_where.arff') + read_weka_res('gram_lists/list_unigram_where.arff')


  multigrams = read_weka_res('gram_lists/list_trigram_bigram_what.arff') + read_weka_res('gram_lists/list_trigram_bigram_when.arff') + read_weka_res('gram_lists/list_trigram_bigram_how.arff') + read_weka_res('gram_lists/list_trigram_bigram_where.arff')

  print multigrams
  unigrams = read_weka_res('gram_lists/list_unigram_what.arff') + read_weka_res('gram_lists/list_unigram_when.arff')  + read_weka_res('gram_lists/list_unigram_how.arff') + read_weka_res('gram_lists/list_unigram_where.arff')

  print len(multigrams)
  print len(unigrams)

  num_yes = 0
  num_no = 0
  tweets = read_tweets("tweets.txt")

  ngrams = read_weka_res('tweetsNew.arff')
  
  try:
    l1=[]
    f = open('unigrams.txt', 'w')
    for gram in unigrams:
      c = 0
      for tweet in tweets:
        if gram.lower() in tweet['text'].lower():
           c+=1
      gram = "'" + gram + "'"
      if c > 0:
        l1.append( {"gram":gram , "freq":c} ) 

    for item in sorted(l1, key=lambda x: x['freq'])[-5:]:
      f.write(item['gram'] + " " +str(item['freq'])+"\n") 

    f.close()
    l1=[]
    f = open('multigrams.txt', 'w')
    for gram in multigrams:
      c = 0
      for tweet in tweets:
        if gram.lower()[1:-1] in tweet['text'].lower():
           c+=1
      if c > 0:
        l1.append({"gram":gram , "freq":c}) 

    for item in sorted(l1, key=lambda x: x['freq'])[-5:]:
      f.write(item['gram'] + " " +str(item['freq'])+"\n") 

    f.close()

  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    sys.exit(1)


  with open('tweetsNew.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar="'", quoting=csv.QUOTE_ALL)

    total_usados = 0
    all_tokens = []
    all_tokens_wstops = []
    maxDate = tweets[-1]['date']
    print maxDate
    i=len(tweets) - 1
    while (maxDate - dateutil.relativedelta.relativedelta(months=3) <  tweets[i]['date'] ):
      tweets[i]['text'] = tweets[i]['text'].lower()
      tweets[i]['text'] = re.sub(r'(?:(?:\d+,?)+(?:\.?\d+)?)', "",tweets[i]['text'])
      tweets[i]['text'] = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', "", tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"http\n",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\n",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\.",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"-",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r":",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r";",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r'\&',' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\"", '\'', tweets[i]['text'])
      tweets[i]['text'] = re.sub(r',',' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r'\[',' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r'\]',' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"'",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\(",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\)",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\'\'",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"`",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"_",' ',tweets[i]['text']) 
      tweets[i]['text'] = re.sub(r"\?",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"¿",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"!",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"¡",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\"",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"‘",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\.",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"/",' ',tweets[i]['text'])
      
      tweets[i]['text'] = re.sub(r"\.\.\.",' ',tweets[i]['text'])      
      tweets[i]['text'] = re.sub(r"\+",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\$",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"%",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"\|",' ',tweets[i]['text'])
      tweets[i]['text'] = re.sub(r"@\w*",' ',tweets[i]['text'])

      yes = False
      for w in what:
        if w in tweets[i]['text']:
          yes = True
          break
      for w in how:
        if w in tweets[i]['text']:
          yes = True
          break
      if yes:
        tweets[i]['crime'] = 'yes'
        spamwriter.writerow([tweets[i]['text'],tweets[i]['crime']])
        num_yes += 1
      else:
        tweets[i]['crime'] = 'no'
        spamwriter.writerow([tweets[i]['text'],tweets[i]['crime']])
        num_no += 1

      i-=1
      total_usados+=1

      # Write csv   
      # if random.random() > 0.5:
      # spamwriter.writerow([tweet['text'],tweet['crime']])
      # else:
      #   spamwriter.writerow([tweet['text'],tweet['crime']])
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

# Esto clasifica los tweets en base a las palabras obtenidas con la herramienta de WEKA.

print "% de yes: ", (num_yes/float(total_usados))*100
print "% de no: ", (num_no/float(total_usados))*100