# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import  HttpResponse
from tweets.models import Tweets
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#raw data tweet imports
import re
import random
import csv
import sys
import string
import codecs
import os

from datetime import datetime
from tweets.models import Tweets
import json


# Create your views here.
def index(request):
    if request.method == 'GET':
        return HttpResponse(serializers.serialize("json",Tweets.objects.all()))
    # elif request.method == 'POST':
    #     pass

def load(request):
    module_dir = os.path.dirname(__file__)  # get current directory
   
    file_path_tweets = os.path.join(module_dir, 'raw_datasets/tweets.txt')
    file_path_keywords = os.path.join(module_dir, 'gram_lists/')
    tweets = read_tweets(file_path_tweets)
   
    # file_path = os.path.join(module_dir, 'raw_datasets/tweets_cleaned.arff')
    # tweets = read_weka_res(file_path)
   

    what = [
    "secuestro","secuestrar","secuestraron","asesinar","asesino","asesinaron","asesinó","violación","violaron","robo","robaron","secuestró","asesinato","extorsión","violación",
    "violaron","mataron","mató"]

    when = [
    "madrugada","noche","día","mañana","tarde","mediodía","noche"
    ]

    how = [
    "quemado","quemaron","quemo","armados","golpes","golpe","golpearon","golpeó","droga","drogas","bombas","tiro","tiros","tiroteado","tiroteados","tirotearon","tiroteo","revolver",
    "puñaladas","puñaladas","pistola","pistolas","plomo","lacrimógenas","lacrimógena","escopeta","escopetas","dispara","disparan","disparando","disparó","dispararon","disparos","cuchillo",
    "cocaína","bomba","bala","balas","armamento","armado","armas","tiroteo","fusil","cuchillo","cuchillos","disparo","fusiles","granada","navaja","ametralladora","bisturí","proyectil",
    "arma blanca","arma de fuego","acuchillado","explosión","cuchilladas","armados","gasolina","incendio"
    ]

    what += read_weka_res(file_path_keywords + 'list_trigram_bigram_what.arff') + read_weka_res(file_path_keywords + 'list_unigram_what.arff')
    when += read_weka_res(file_path_keywords + 'list_trigram_bigram_when.arff') + read_weka_res(file_path_keywords + 'list_unigram_when.arff')
    how += read_weka_res(file_path_keywords + 'list_trigram_bigram_how.arff') + read_weka_res(file_path_keywords +  'list_unigram_how.arff')

    reload(sys)
    sys.setdefaultencoding("utf-8")

    num_yes = 0
    num_no = 0
    created = 0
    failed= 0
    for tweet in tweets:
      
      tweet['text'] = tweet['text'].lower()
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

      yes = False
      
      tweet['what'] = ''
      tweet['how'] = ''
      for w in what:
        if w in tweet['text']:
          yes = True
          tweet['what'] = w
          break
      for w in how:
        if w in tweet['text']:
          yes = True
          tweet['how'] = w
          break
      if yes:
        tweet['crime'] = 'yes'
        num_yes += 1
        #crear nueva instancia de Tweet.
        try : 
          #[2016-10-18 20:31:29]
          print "Creando tweet:", tweet
          date = datetime.strptime(tweet['date'], '%Y-%m-%d %H:%M:%S')
          t = Tweets.objects.create_tweet(texto=tweet['text'],
                                     fecha=date, 
                                     que=tweet['what'], 
                                     como=tweet['how'])
          print t
          t.save()
          created +=1
        except:
          failed +=1
          pass

      else:
        tweet['crime'] = 'no'
        num_no += 1



    print "% de yes: ", (num_yes/float(len(tweets)))*100
    print "% de no: ", (num_no/float(len(tweets)))*100


    return JsonResponse({"created":created, "failed": failed})

@csrf_exempt
def textSize(request):
  module_dir = os.path.dirname(__file__)  # get current directory
   
  file_path_keywords = os.path.join(module_dir, 'gram_lists/')
  file_path_tweets = os.path.join(module_dir, 'raw_datasets/tweets.txt')
  tweets = read_tweets(file_path_tweets)
 
  # file_path = os.path.join(module_dir, 'raw_datasets/tweets_cleaned.arff')
  # tweets = read_weka_res(file_path)
 

  what = [
  "secuestro","secuestrar","secuestraron","asesinar","asesino","asesinaron","asesinó","violación","violaron","robo","robaron","secuestró","asesinato","extorsión","violación",
  "violaron","mataron","mató"]

  when = [
  "madrugada","noche","día","mañana","tarde","mediodía","noche"
  ]

  how = [
  "quemado","quemaron","quemo","armados","golpes","golpe","golpearon","golpeó","droga","drogas","bombas","tiro","tiros","tiroteado","tiroteados","tirotearon","tiroteo","revolver",
  "puñaladas","puñaladas","pistola","pistolas","plomo","lacrimógenas","lacrimógena","escopeta","escopetas","dispara","disparan","disparando","disparó","dispararon","disparos","cuchillo",
  "cocaína","bomba","bala","balas","armamento","armado","armas","tiroteo","fusil","cuchillo","cuchillos","disparo","fusiles","granada","navaja","ametralladora","bisturí","proyectil",
  "arma blanca","arma de fuego","acuchillado","explosión","cuchilladas","armados","gasolina","incendio"
  ]


  what += read_weka_res(file_path_keywords + 'list_trigram_bigram_what.arff') + read_weka_res(file_path_keywords + 'list_unigram_what.arff')
  when += read_weka_res(file_path_keywords + 'list_trigram_bigram_when.arff') + read_weka_res(file_path_keywords + 'list_unigram_when.arff')
  how += read_weka_res(file_path_keywords + 'list_trigram_bigram_how.arff') + read_weka_res(file_path_keywords +  'list_unigram_how.arff')

  reload(sys)
  sys.setdefaultencoding("utf-8")

  res = {"children":[]}
  word_set = []

  # print what
  # print when
  # print how, "\n"

  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)
  zona = body['zona']

  tweets = Tweets.objects.all()
  # print tweets, "\n"
  i = 0
  for w in what:
    freq = 0
    res["children"].append({})
    res["children"][i]["name"] = w
    for tweet in tweets:
      if zona !="Todas":
        if w in tweet.texto and zona in tweet.texto: 
          freq += 1
      else:
        if w in tweet.texto: 
          freq += 1
    res["children"][i]["freq"] = freq
    res["children"][i]["type"] = "what"
    i += 1
  for w in how:
    freq = 0
    res["children"].append({})
    res["children"][i]["name"] = w
    for tweet in tweets:
      if zona !="Todas":
        if w in tweet.texto: 
          freq += 1
      else:
        if w in tweet.texto: 
          freq += 1
    res["children"][i]["freq"] = freq
    res["children"][i]["type"] = "how"
    i += 1

  print res, "\n"


  return HttpResponse(json.dumps(res))

@csrf_exempt
def heatMap(request):
  #data format:
  #word day value 

  module_dir = os.path.dirname(__file__)  # get current directory
   
  file_path_keywords = os.path.join(module_dir, 'gram_lists/')
  file_path_tweets = os.path.join(module_dir, 'raw_datasets/tweets.txt')
  tweets = read_tweets(file_path_tweets)
 
  # file_path = os.path.join(module_dir, 'raw_datasets/tweets_cleaned.arff')
  # tweets = read_weka_res(file_path)
 

  what = [
  "secuestro","secuestrar","secuestraron","asesinar","asesino","asesinaron","asesinó","violación","violaron","robo","robaron","secuestró","asesinato","extorsión","violación",
  "violaron","mataron","mató"]

  when = [
  "madrugada","noche","día","mañana","tarde","mediodía","noche"
  ]

  how = [
  "quemado","quemaron","quemo","armados","golpes","golpe","golpearon","golpeó","droga","drogas","bombas","tiro","tiros","tiroteado","tiroteados","tirotearon","tiroteo","revolver",
  "puñaladas","puñaladas","pistola","pistolas","plomo","lacrimógenas","lacrimógena","escopeta","escopetas","dispara","disparan","disparando","disparó","dispararon","disparos","cuchillo",
  "cocaína","bomba","bala","balas","armamento","armado","armas","tiroteo","fusil","cuchillo","cuchillos","disparo","fusiles","granada","navaja","ametralladora","bisturí","proyectil",
  "arma blanca","arma de fuego","acuchillado","explosión","cuchilladas","armados","gasolina","incendio"
  ]


  what += read_weka_res(file_path_keywords + 'list_trigram_bigram_what.arff') + read_weka_res(file_path_keywords + 'list_unigram_what.arff')
  how += read_weka_res(file_path_keywords + 'list_trigram_bigram_how.arff') + read_weka_res(file_path_keywords +  'list_unigram_how.arff')

  reload(sys)
  sys.setdefaultencoding("utf-8")

  res = {"como":[], "que":[]}

  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)
  zona = body['zona']

  comos = Tweets.objects.exclude(como__isnull=True).exclude(como__exact='')
  ques = Tweets.objects.exclude(que__isnull=True).exclude(que__exact='')

  for w in what:
    l = [[w,1,0],[w,2,0],[w,3,0],[w,4,0],[w,5,0],[w,6,0],[w,7,0]]
    for tweet in ques:
      if zona !="Todas":
        if w in tweet.texto and zona in tweet.texto: 
          if tweet.fecha.weekday() == 0: 
            l[0][2] +=1 
          elif  tweet.fecha.weekday() == 1:
            l[1][2] +=1 
          elif  tweet.fecha.weekday() == 2: 
            l[2][2] +=1
          elif  tweet.fecha.weekday() == 3: 
            l[3][2] +=1
          elif  tweet.fecha.weekday() == 4: 
            l[4][2] +=1
          elif  tweet.fecha.weekday() == 5: 
            l[5][2] +=1
          elif  tweet.fecha.weekday() == 6: 
            l[6][2] +=1
      else:
        if w in tweet.texto: 
          if tweet.fecha.weekday() == 0: 
            l[0][2] +=1 
          elif  tweet.fecha.weekday() == 1:
            l[1][2] +=1 
          elif  tweet.fecha.weekday() == 2: 
            l[2][2] +=1
          elif  tweet.fecha.weekday() == 3: 
            l[3][2] +=1
          elif  tweet.fecha.weekday() == 4: 
            l[4][2] +=1
          elif  tweet.fecha.weekday() == 5: 
            l[5][2] +=1
          elif  tweet.fecha.weekday() == 6: 
            l[6][2] +=1
    res["que"] += l  

  for w in how:
    l = [[w,1,0],[w,2,0],[w,3,0],[w,4,0],[w,5,0],[w,6,0],[w,7,0]]
    for tweet in comos:
      if zona != "Todas":
        if w in tweet.texto and zona in tweet.texto:
          if tweet.fecha.weekday() == 0: 
            l[0][2] +=1 
          elif  tweet.fecha.weekday() == 1:
            l[1][2] +=1 
          elif  tweet.fecha.weekday() == 2: 
            l[2][2] +=1
          elif  tweet.fecha.weekday() == 3: 
            l[3][2] +=1
          elif  tweet.fecha.weekday() == 4: 
            l[4][2] +=1
          elif  tweet.fecha.weekday() == 5: 
            l[5][2] +=1
          elif  tweet.fecha.weekday() == 6: 
            l[6][2] +=1
      else:     
        if w in tweet.texto: 
          if tweet.fecha.weekday() == 0: 
            l[0][2] +=1 
          elif  tweet.fecha.weekday() == 1:
            l[1][2] +=1 
          elif  tweet.fecha.weekday() == 2: 
            l[2][2] +=1
          elif  tweet.fecha.weekday() == 3: 
            l[3][2] +=1
          elif  tweet.fecha.weekday() == 4: 
            l[4][2] +=1
          elif  tweet.fecha.weekday() == 5: 
            l[5][2] +=1
          elif  tweet.fecha.weekday() == 6: 
            l[6][2] +=1
    res["como"] += l  


  return HttpResponse(json.dumps(res))


def read_weka_res(name):
  try:
    # f = open(name, 'r') 
    f = codecs.open(name, encoding='utf-8')
    data = f.readlines()
    i = 0
    res = []
    for line in data:
      if i > 2:
        if line[0] == "@":
          l = line.split("-")
          if len(l) > 1:
            res.append(l[1])
      i += 1
    f.close()
    return res
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    sys.exit(1)


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
        info[1] = info[1]
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
