# by Richi Rod AKA @richionline / falken20

import os
import logging
import sys
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import pytz  # Work with time zones
from telegram_client import TelegramDeliveryError, send_telegram_message


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load env file
load_dotenv(find_dotenv())
# load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)

# Set log level and secret key
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))
SECRET_KEY = os.getenv('SECRET_KEY', default='xsd--ammmss!!"kd(sss')

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
        logging.error(
            f'{os.getenv("ID_LOG", "")} ERROR scrapping web at line '
            f'{sys.exc_info()[2].tb_lineno}: {type(err).__name__}')
        return None


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
        logging.error(
            f'{os.getenv("ID_LOG", "")} ERROR saving weather data at line '
            f'{sys.exc_info()[2].tb_lineno}: {type(err).__name__}')
        return None


def parrao_weather_bot(request):
    """Fetch and publish scraped weather through Telegram."""
    try:
        dict_weather_data = get_weather_data()
        if dict_weather_data is None:
            return "Could not retrieve weather", 502

        tz_MAD = pytz.timezone('Europe/Madrid')
        message = (
            f'Weather at {datetime.now(tz_MAD).strftime("%Y-%m-%d %H:%M")}\n'
            f'🌞 Puesta sol\n'
            f'🌡 {dict_weather_data[POSITION_TEMP]["Value"].replace(" ", "")}\n'
            f'🌧 {dict_weather_data[POSITION_RAIN]["Value"].replace(" ", "")}\n'
            f'💧 {dict_weather_data[POSITION_HUMI]["Value"].replace(" ", "")} '
            f'humidity\n'
            f'💨 {dict_weather_data[POSITION_WIND]["Value"].replace(" ", "")}\n'
            f'Source: {SOURCE}'
        )

        if os.getenv("ENV_PRO", "N") == "Y":
            send_telegram_message(message)
        else:
            logging.info("Dry run; Telegram message not sent:\n%s", message)
        return "Message sent", 200
    except TelegramDeliveryError as err:
        logging.error("Telegram delivery failed: %s", err)
        return "Telegram delivery failed", 502

    except Exception as err:
        logging.error("Weather publication failed: %s", type(err).__name__)
        return "Weather publication failed", 502


if __name__ == '__main__':

    print('***** Starting cron *****')
    parrao_weather_bot({})
    print('***** Shutdown cron *****')
