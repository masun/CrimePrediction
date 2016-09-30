import sys

def read_tweets(name):
  try:
    f = open(name, 'r') 
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
        info[1] = info[1].decode("utf-8", "ignore")
        info[2] = info[2][:-1] # Removing "\n"
        info[2] = info[2][:-1] # Removing "]"
        tweets.append(info)
    f.close()
    return tweets
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    sys.exit(1)

if __name__ == "__main__":
  for elem in read_tweets("prueba.txt"):
    print elem[1].encode('utf-8')