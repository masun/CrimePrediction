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
"CCSTheaterClub",
"noticias24",
"laguiadecaracas",
"VenezuelainJpn",
"EmbaFrancia",
"usembassyve",
"EmbCanVenezuela",
"ConsEspCaracas",
"EmbajadaRusaVen",
"UKinVenezuela",
"EmbamexVen",
"minculturave",
"teresacarreno",
"LaPatanaCcs",
"EvenVenezuela",
"VzlaExpoTattoo",
"vzlasinfonica",
"elsistema",
"expodato",
"SuperEventosVE"
]

# usersList = [
# "laguiadecaracas",
# "ElNacionalWeb",
# "culturachacao",
# "ExpoGastronomia",
# "ElUniversal",
# "LaGuiaDelDia",
# "TICKETMUNDO",
# "trasnochocult",
# "CCulturalBOD",
# "ElHatillo",
# "UrbanCuple",
# "hoyquehay"
# ]

def limits(l):
    if len(l)==0:
        return []
    maxId = l[0].id
    minId = l[0].id
    for status in l:
        print(status.id)
        if status.id > maxId:
            maxId = status.id
        if status.id < minId:
            minId = status.id
    return [minId, maxId]


for user in usersList:
    print('Pidiendo tweets del usuario:')
    print(user)
    print("\n")
    tweets = []
    tl = api.user_timeline(screen_name=user, count=20)
    tweets = tweets + tl
    l = limits(tl) 
    print("Se lograron obtener 20 tweets del usuario")
    i = 0
    while(i < 50):
        try :
            #Arreglar esta llamada para retornar twwts diferents, posiblemente con max_id y since_id
            tl = api.user_timeline(screen_name=user, count=20, max_id= l[0])
            # time.sleep(5)
            # print("Se hizo el request correctamente..")
            print (len(tl))
            i += 1
            l = limits(tl)
            print(l)
            tweets = tweets + tl 
            print("Se lograron obtener 20 tweets del usuario")
        except:
            print('Error al hacer request a Twitter.Esperando..')
            time.sleep(60*60)
            pass
    
    f = open('tweets.txt','a')
    f.write(user)
    f.write(":\n")
    for tweet in tweets:
        f.write("[")
        f.write(str(tweet.created_at))
        f.write("]")
        f.write("[")
        f.write(tweet.text.encode('utf-8'))
        f.write("]")
        f.write("[")
        f.write(str(tweet.retweet_count))
        f.write("]")
        f.write("\n")
    f.write("-\n")
    f.close()
   
