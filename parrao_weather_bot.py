# by Richi Rod AKA @richionline / falken20

import os
import tweepy
import logging
import sys
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import pytz  # Work with time zones

import requests
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load env file
load_dotenv(find_dotenv())
# load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)

# Set log level and secret key
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))
SECRET_KEY = os.getenv('SECRET_KEY', default='xsd--ammmss!!"kd(sss')

# Credentials for twitter API
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Weather station API data
STATION_ID = os.environ.get('STATION_ID')
API_KEY = os.environ.get('API_KEY')
URL_WEATHER = f"https://api.weather.com/v2/pws/observations/current?stationId={STATION_ID}" \
    f"&format=json&units=m&numericPrecision=decimal" \
    f"&apiKey={API_KEY}"
SOURCE = "Personal weather station in Cercedilla"


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
        response = requests.get(URL_WEATHER)
        dict_weather = json.loads(response.text)

        logging.info(
            f'{os.getenv("ID_LOG", "")} Weather data JSON: \n {dict_weather}')

        return dict_weather["observations"][0]
    except Exception as err:
        logging.error(
            f'{os.getenv("ID_LOG", "")} ERROR saving weather data at line {sys.exc_info()[2].tb_lineno}: {err}')
        return None


def parrao_weather_bot(request):
    """ Method for publishing weather data in Twitter """

    logging.info(f'{os.getenv("ID_LOG", "")} Getting Twitter credentials')
    api = get_auth()
    try:
        api.verify_credentials()
        logging.info(
            f'{os.getenv("ID_LOG", "")} Twitter authentication succesfully')
    except Exception as err:
        logging.error(
            f'{os.getenv("ID_LOG", "")} Error getting Twitter credentials: \n {format(err)}')

    # Get the current weather data and post the tweet
    try:
        dict_weather_data = get_weather_data()
        logging.info(
            f'{os.getenv("ID_LOG", "")} Preparing tweet...')
        tz_MAD = pytz.timezone('Europe/Madrid')
        tweet = f'Weather in Cercedilla🇪🇸 at {datetime.now(tz_MAD).strftime("%Y-%m-%d %H:%M")}\n' \
                f'🌡 {dict_weather_data["metric"]["temp"]}º \n' \
                f'🌧 {dict_weather_data["metric"]["precipTotal"]} mm \n' \
                f'💧 {dict_weather_data["humidity"]} % \n' \
                f'💨 {dict_weather_data["metric"]["windSpeed"]} km/h \n' \
                f'🌞 {dict_weather_data["uv"]} UVI \n' \
                f'Source: {SOURCE}'

        logging.info(f'{os.getenv("ID_LOG", "")} Starting to post the tweet')
        if os.getenv("ENV_PRO", "N") == "Y":
            logging.info(f'{os.getenv("ID_LOG", "")} Posting tweet in Tweeter...')
            api.update_status(tweet)
        else:
            logging.debug(f"\n************* TWEET:\n{tweet}\n*****************")
        logging.info(
            f'{os.getenv("ID_LOG", "")} Post tweet succesfully:\n{tweet}')

    except Exception as err:
        logging.error(
            f'{os.getenv("ID_LOG", "")} Error trying to post the tweet of weather data: \n {format(err)}')


if __name__ == '__main__':

    print('***** Starting cron *****')
    parrao_weather_bot({})
    print('***** Shutdown cron *****')
