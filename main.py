# by Richi Rod AKA @richionline / falken20

import os
import tweepy
import logging
import sys
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import pytz  # Work with time zones


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load env file
load_dotenv(find_dotenv())
#load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)

# Set log level and secret key
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))
SECRET_KEY = os.getenv('SECRET_KEY', default='xsd--ammmss!!"kd(sss')

# Credentials for twitter API
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

URL_WEATHER = 'http://meteomad.net/estaciones/cercedilla/cercedilla.htm'
SOURCE = 'Estación Termopluviométrica de J.V.D'
# This constant is for to know the position in the dict of the values
POSITION_TEMP = 0
POSITION_RAIN = 5
POSITION_HUMI = 1
POSITION_WIND = 3


def scrap_web(url):
    """
    For getting data weather of a specific url
    :param url: The url of a specific web
    """
    try:
        data = pd.read_html(url)
        df = data[0]

        logging.info(f'{os.getenv("ID_LOG", "")} url scrapping: {url}')
        logging.debug(f'{os.getenv("ID_LOG", "")} Data to scrap:\n {data[0]}')

        # Cleaning the info it doesn't neccesary
        df = df.drop([4], axis=1)  # axis is the column name
        df = df.drop([0, 1, 2, 3, 4, 5])

        # Get seveal rows and cols
        df = df.iloc[0:6, [0, 1]]

        # We can change the name of the columns
        df.columns = ('Parameter', 'Value')

        # Clean and restore the index number because it is kind of
        # annoying but it is not necessary
        df = df.reset_index(drop=True)

        logging.info(f'{os.getenv("ID_LOG", "")} Data scrapped:\n {df}')

        return df

    except Exception as err:
        logging.error(f'{os.getenv("ID_LOG", "")} ERROR scrapping web at line {sys.exc_info()[2].tb_lineno}: {err}')
        return None        


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
        df_weather = scrap_web(URL_WEATHER)
        # Transform to a list of dict, each dict with "Parameter" and "Value"
        dict_weather = df_weather.to_dict(orient='records')

        return dict_weather
    except Exception as err:
        logging.error(f'{os.getenv("ID_LOG", "")} ERROR saving weather data at line {sys.exc_info()[2].tb_lineno}: {err}')
        return None


def parrao_weather_bot(request):
    """ Method for publishing weather data in Twitter """
    
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
        tz_MAD = pytz.timezone('Europe/Madrid') 
        tweet = f'Weather at {datetime.now(tz_MAD).strftime("%Y-%m-%d %H:%M")} -> ' \
                f'{dict_weather_data[POSITION_TEMP]["Value"].replace(" ", "")} - ' \
                f'{dict_weather_data[POSITION_RAIN]["Value"].replace(" ", "")} - ' \
                f'{dict_weather_data[POSITION_HUMI]["Value"].replace(" ", "")} humidity - ' \
                f'{dict_weather_data[POSITION_WIND]["Value"].replace(" ", "")}' \
                f'\nSource: {SOURCE}'

        api.update_status(tweet)
        logging.info(f'{os.getenv("ID_LOG", "")} Post tweet succesfully: \n {tweet}')

    except Exception as err:
        logging.error(f'{os.getenv("ID_LOG", "")} Error trying to post the tweet of weather data: \n {format(err)}')


if __name__ == '__main__':

    print(f'***** Starting cron *****')
    parrao_weather_bot({})
    print(f'***** Shutdown cron *****')