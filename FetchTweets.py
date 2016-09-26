import tweepy
from tweepy import OAuthHandler
import time
 

consumer_key = 'yyHq8kH2AZtaT4UZikVVblEof'
consumer_secret = 'S9tuxzPOcQRUBM5A1Mr0ixLzBZfjpTbeqbGIGnKGj7BW8JXcXe'
access_token = '1253448288-iJAO60J8eJmUgMbjNjaAm0KJKxxnG2F5WK8hAgb'
access_secret = 'ZVDUIfgXJyUHxWp89DrcdQX91uOdH2UHGMysb7KjeQezE'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

usersList = [
"laguiadecaracas",
"ElNacionalWeb",
"culturachacao",
"ExpoGastronomia",
"ElUniversal",
"LaGuiaDelDia",
"TICKETMUNDO",
"trasnochocult",
"CCulturalBOD",
"ElHatillo",
"UrbanCuple",
"hoyquehay"
]

def limits(l):
    maxId = l[0].id
    minId = l[0].id
    for status in l:
        if status.id > maxId:
            maxId = status.id
        if status.id < minId:
            minId = status.id
    return (minId, maxId)


for user in usersList:
    print('Pidiendo tweets del usuario:')
    print(user)
    print("\n")
    tweets = []
    # time.sleep(15*60)
    tl = api.user_timeline(screen_name=user, count=20)
    tweets = tweets + tl
    (minId,maxId) = limits(tl) 
    print("Se lograron obtener 20 tweets del usuario")
    i = 0
    while(i < 50):
        try :
            tl = api.user_timeline(screen_name=user, count=20, since_id=maxId, max_id=minId)
            print("entre")
            i += 1
            print("entre2")
            
            (minId,maxId) = limits(tl)    
            print("entre3")
            
            tweets = tweets + tl 
            print("Se lograron obtener 20 tweets del usuario")
        except:
            print('Error al hacer request a Twitter.Esperando..')
            # time.sleep(15*60)
            pass
    try:
        f = open('tweets.txt','a')
        f.write(user)
        f.write("\n")
        for tweet in tweets:
            f.write(tweet.created_at)
            f.write("\n")
            f.write(tweet.hashtags)
            f.write("\n")
            f.write(tweet.text)
            f.write("\n")
            f.write(tweet.retweet_count)
            f.write(",")
            f.write("\n")
        f.write("-\n")
        f.close()
    except:
        print 'Error al tratar de guardar los datos en el archivo'

# print('Pidiendo tweets del usuario:')
# print("\n")
# tweets = []
# # time.sleep(15*60)
# tl = api.user_timeline(screen_name=usersList[0], count=20)
# tweets = tweets + tl
# (minId,maxId) = limits(tl) 
# print("Se lograron obtener 20 tweets del usuario")
# tl = api.user_timeline(screen_name=usersList[0], count=20, since_id=maxId, max_id=minId)
# tweets = tweets + tl 