# by Richi Rod AKA @richionline / falken20

import os
import tweepy

# Credentials for twitter API
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


# Method to get user authentication in Twitter
def get_auth():
    """Get user credentials in Twitter"""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def parrao_weather_bot():
    """ Process to create a bot for publishing weather data in Twitter """
    # api = get_auth()
