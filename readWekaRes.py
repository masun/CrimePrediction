import codecs
import sys

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
          l = line.split(" ")
          if len(l) > 1:
            if (l[1][0] == "'"):
              if (l[2][-1] == "'"):
                res.append(l[1] + " " + l[2])
              else:
                res.append(l[1] + " " + l[2] + " " + l[3])
            else:
              res.append(l[1])
      i += 1
    f.close()
    return res
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    sys.exit(1)