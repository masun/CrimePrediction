from nltk.corpus import stopwords


f = open('stopwords_spanish.txt','a')

for word in stopwords.words('spanish'):
    f.write(word.encode('utf8'))
    f.write("\n")