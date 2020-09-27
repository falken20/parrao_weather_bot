# by Richi Rod AKA @richionline / falken20

import tweepy
import csv
import json
import pandas as pd
import string
import re

###################################
##### Search with API Twitter #####
###################################

def search_with_API_twitter(api):
    """Search with API Twitter"""
    # Create the CSV file
    csvFile = open(NOMBRE_FICHERO, 'w')
    csvWriter = csv.writer(csvFile)

    # Create the consult
    # Help for complex consulting:
    # https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators
    # We set the text to search and more filters in var query
    query = "#bonjovi -filter:retweets until:2020-05-10"
    number_of_tweets = 5
    language = 'es'

    # Get and processing the results of Twitter API
    # Twitter API help:
    # https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
    csvWriter.writerow(["Created_at", "User_name", "Location", "Tweet"])
    print('>>>>> Getting tweets...')
    for tweet in tweepy.Cursor(api.search,
                               q=query,
                               count=number_of_tweets,
                               lang=language,
                               since="2020-05-09").items():
        print(tweet.created_at, tweet.user.screen_name, tweet.user.location, tweet.text)
        csvWriter.writerow([tweet.created_at, tweet.user.screen_name, tweet.user.location,
                            tweet.text.encode('utf-8')])


#############################################
##### Streaming the tweets in real time #####
#############################################

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text.encode("ascii", errors='replace'))  # Console output compatible con UTF-8 (emojis)
        print("=" * 10)

    def on_data(self, data):
        try:
            decoded = json.loads(data)
            if decoded['lang'] == 'es':
                print(">> Se ha detectado un tweet en ingles que cumple los filtros:")
                print(decoded)
                dict_ = {'user': [], 'user_location': [], 'date_created': [], 'text': [],
                         'retweet_count': [], 'favorite_count': [], 'hashtags': [],
                         'user_mentions': [], 'urls': []}
                dict_['user'].append(decoded['user']['screen_name'])
                dict_['user_location'].append(decoded['user']['location'])
                dict_['date_created'].append(decoded['created_at'])
                dict_['retweet_count'].append(decoded['retweet_count'])
                dict_['favorite_count'].append(decoded['favorite_count'])
                dict_['text'].append(decoded['text'])
                dict_['hashtags'].append(decoded['entities']['hashtags'])
                dict_['user_mentions'].append(decoded['entities']['user_mentions'])
                dict_['urls'].append(decoded['entities']['urls'])

                df = pd.DataFrame(dict_)
                # Si queremos ordenar los tweets por algun valor
                # df.sort_values(by='retweet_count', inplace=True, ascending=False)

                # creamos y pasamos los datos capturados a un csv
                df.to_csv(path_or_buf=NOMBRE_FICHERO_2, mode="a", header=False, encoding="utf-8")

            else:
                print(">> Tweet descartado por idioma diferente")

        except Exception as e:
            print("ERROR: {}".format(e))
        finally:
            return True  # Bucle que me permite seguir escuchando


def streaming_tweets_in_real_time(api, hashtag):
    # Nos conectamos al stream
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    print(">>>>> Listening tweets...")

    # Se puede filtrar por hashtag o por location
    # para conseguir una zona de coordenadas como locations=[-123.26,33.75,-115.72,38.35]
    # o locations=[-180,-90,180,90] dirigirse a https://boundingbox.klokantech.com/
    myStream.filter(track=[hashtag])


##################################
##### Cleaning the text. NLP #####
##################################

def clean_tweet(tweet):
    """Clean a string"""
    tweet = re.sub('http\S+\s*', '', tweet)  # remove URLs
    tweet = re.sub('RT|cc', '', tweet)  # remove RT and cc
    tweet = re.sub('#\S+', '', tweet)  # remove hashtags
    tweet = re.sub('@\S+', '', tweet)  # remove mentions
    tweet = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), '', tweet)  # remove punctuations
    tweet = re.sub('\s+', ' ', tweet)  # remove extra whitespace
    return tweet

def cleaning_the_text_NLP():
    """Cleaning the text. NLP"""
    original_tweet = "RT MARAVILLOSO 👏👏 Siempre 'I… https://t.co/XVEXKQq9Yq"
    print('Original text ==> ', original_tweet)

    print('\n>>>>> Decodificar los datos')
    texto = original_tweet.encode("ascii", "ignore")
    texto = str(texto, 'utf-8')
    print('RESULT ==> ', texto)

    print('\n>>>>> Eliminar puntuaciones')
    print('Punctuation: ', string.punctuation)
    translator = str.maketrans('', '', string.punctuation)
    print('translator var ==> ', translator)
    print('translate(translator) ==> ', texto.translate(translator))
    print('RESULT ==> ', texto)

    print('\n>>>>> Eliminar urls, rt, hashtags, mentions, etc...')
    print('RESULT (Texto anterior) ==> ', clean_tweet(texto))
    print('RESULT (Texto original) ==> ', clean_tweet(original_tweet))


#########################################
##### Cleaning the text with Lambda #####
#########################################

def cleaning_the_text_lambda():
    """Cleaning the text with Lambda"""
    data = pd.read_csv(NOMBRE_FICHERO, encoding="ISO-8859-1")
    print('>>>>> Head from csv file\n', data.head(3))

    print('\n>>>>> Eliminamos signos de puntuación con función lambda')
    texto = data['Tweet'].map(lambda a: a.translate(string.punctuation))
    print(texto)

    print('\n>>>>> Unificamos a ascii')
    texto = texto.map(lambda a: a.lower())
    print(texto)

    print('\n>>>>> Eliminamos la url y rt')
    texto = texto.map(lambda a: re.sub(r"http\S+", "", a))
    texto = texto.map(lambda a: re.sub(r"rt", "", a))
    print(texto)

    print('\n>>>>> Pasamos todo a minúscula y lo guardamos en el dataset y en nuevo csv')
    data['Tweet'] = texto
    data.to_csv(NOMBRE_FICHERO_CLEAN)
    print(data.head(3))


######################
##### Word count #####
######################

def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


def wordcount():
    """Examples about counting words"""
    example = "mi prueba es una prueba buena"
    res = word_count(example)
    print('\n>>>>> Contamos las palabras del string "%s": %s' % (example, res))

    type(res)
    orden = sorted(res.items(), key=lambda x: x[1])
    print('\n>>>>> Ordenamos el resultado: %s' % orden)

    data = pd.read_csv(NOMBRE_FICHERO, encoding="ISO-8859-1")
    midata = data['Tweet']
    text_total = ' '.join(midata)
    resultado = word_count(text_total)
    orden = sorted(resultado.items(), key=lambda x: x[1])
    res = orden[len(orden) - 5:len(orden)]
    print('\n>>>>> Ahora buscamos la palabra más repetida en nuestro fichero de hastags: %s' % res)


def wordcloud():
    # Hacer la nube de tags
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    data = pd.read_csv(NOMBRE_FICHERO, encoding="ISO-8859-1")
    wc = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(data.Tweet[10])
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    text = " ".join(review for review in data.Tweet)
    # Generate a word cloud image
    wc = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()

#####################
##### Main call #####
#####################

# Twitter keys and tokens
CONSUMER_KEY = 'PM9pz5JncC7EwU8It2A2TNdrp'
CONSUMER_SECRET = 'S0xrR3gikijLxJzfszpI2c2sCApMjgk3Nr9PHzbkfyFuBmSECO'
ACCESS_TOKEN = '171492732-Z8MAQnxihwwkuVuuqP4qIqzKpR1nzDiTzte4ICZA'
ACCESS_TOKEN_SECRET = '25PXLhUl19mMJbJAdhMvhlRmtC2wYtCYYNRnEGFWIpszR'

HASHTAG = '#felizmiercoles'
NOMBRE_FICHERO = 'tests/richi_tweets.csv'
NOMBRE_FICHERO_2 = 'tests/richi_tweets_2.csv'
NOMBRE_FICHERO_CLEAN = 'tests/richi_tweets_clean.csv'


# Method to get user authentication in Twitter
def get_auth():
    """Get user credentials in Twitter"""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


if __name__ == '__main__':
    # Get the credentials for Twitter API
    api = get_auth()  # Build an API object.

    print('\n=================== Search with API Twitter ===================\n')
    search_with_API_twitter(api)

    print('\n=================== Streaming the tweets in real time by hashtag or location '
          '===================\n')
    # streaming_tweets_in_real_time(api, HASHTAG)

    print('\n=================== Cleaning the text. NLP ===================\n')
    cleaning_the_text_NLP()

    print('\n=================== Cleaning the text with Lambda ===================\n')
    cleaning_the_text_lambda()

    print('\n=================== Wordcount examples ===================\n')
    wordcount()

    print('\n=================== Wordcloud examples ===================\n')
    wordcloud()
