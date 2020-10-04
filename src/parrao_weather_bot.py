# by Richi Rod AKA @richionline / falken20

import os
import tweepy
import logging
import sys
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

from . import utils

# Load env file
load_dotenv(find_dotenv())
# Set log level
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))

# Credentials for twitter API
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

URL_WEATHER = 'http://meteomad.net/estaciones/cercedilla/cercedilla.htm'
# This constant is for to know the position in the dict of the values
POSITION_TEMP = 0
POSITION_RAIN = 5
POSITION_HUMI = 1
POSITION_WIND = 3

def get_auth():
    """Get user credentials in Twitter"""

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def get_weather_data():
    """ Process to get current weather data  """
    logging.info(f'{os.getenv("ID_LOG", "")} Getting weather data...')

    try:
        # Getting a dataframe with the all data weather
        df_weather = utils.scrap_web(URL_WEATHER)
        # Transform to a list of dict, each dict with "Parameter" and "Value"
        dict_weather = df_weather.to_dict(orient='records')

        return dict_weather
    except Exception as err:
        logging.error(f'{os.getenv("ID_LOG", "")} ERROR saving weather data at line {sys.exc_info()[2].tb_lineno}: {error}')
        return None


def parrao_weather_bot():
    """ Process to create a bot for publishing weather data in Twitter """
    
    logging.info(f'{os.getenv("ID_LOG", "")} Getting Twitter credentials')
    api = get_auth()
    try:
        api.verify_credentials()
        logging.info(f'{os.getenv("ID_LOG", "")} Twitter authentication succesfully')
    except Exception as err:
        logging.error(f'{os.getenv("ID_LOG", "")} Error getting Twitter credentials: \n {format(err)}')

    # Get the current weather data and post the tweet
    try:
        dict_weather_data = get_weather_data()
        print(dict_weather_data)
        tweet = f'Cercedilla weather at {datetime.now().strftime("%Y-%m-%d %H:%M")} -> ' \
                f'{dict_weather_data[POSITION_TEMP]["Value"].replace(" ", "")} - ' \
                f'{dict_weather_data[POSITION_RAIN]["Value"].replace(" ", "")} - ' \
                f'{dict_weather_data[POSITION_HUMI]["Value"].replace(" ", "")} humidity - ' \
                f'{dict_weather_data[POSITION_WIND]["Value"].replace(" ", "")}'

        api.update_status(tweet)
        logging.info(f'{os.getenv("ID_LOG", "")} Post tweet succesfully: \n {tweet}')

    except Exception as err:
        logging.error(f'{os.getenv("ID_LOG", "")} Error trying to post the tweet of weather data: \n {format(err)}')

