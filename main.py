# by Richi Rod AKA @richionline / falken20

import os
import logging
import sys
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import pytz  # Work with time zones

import requests

from models import Weather
from telegram_client import TelegramDeliveryError, send_telegram_message


load_dotenv(find_dotenv())

logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))

# Weather station API data
STATION_ID = os.environ.get('STATION_ID')
API_KEY = os.environ.get('API_KEY')
URL_WEATHER = (
    "https://api.weather.com/v2/pws/observations/current?"
    f"stationId={STATION_ID}&format=json&units=m&numericPrecision=decimal"
    f"&apiKey={API_KEY}"
)
URL_WEATHER_DAILY = (
    "https://api.weather.com/v2/pws/history/daily?"
    f"stationId={STATION_ID}&format=json&units=m&numericPrecision=decimal"
    f"&apiKey={API_KEY}&date="
)
SOURCE = "Falken weather station"


def get_api_data(url=URL_WEATHER):
    """Fetch the first weather observation from the API."""
    logging.info(f'{os.getenv("ID_LOG", "")} Getting weather data...')

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()["observations"][0]
    except Exception as err:
        logging.error(
            f'{os.getenv("ID_LOG", "")} ERROR getting weather data at line '
            f'{sys.exc_info()[2].tb_lineno}: {type(err).__name__}')
        return None


def _publish_message(message):
    if os.getenv("ENV_PRO", "N") != "Y":
        logging.info("Dry run; Telegram message not sent:\n%s", message)
        return "Dry run; message not sent", 200
    try:
        send_telegram_message(message)
    except TelegramDeliveryError as err:
        logging.error("Telegram delivery failed: %s", err)
        return "Telegram delivery failed", 502

    logging.info("Telegram message sent successfully:\n%s", message)
    return "Message sent", 200


def parrao_weather_bot(request):
    """Fetch and publish current weather through Telegram."""
    logging.info("%s Fetching current weather...", os.getenv("ID_LOG", ""))
    weather_data = get_api_data(URL_WEATHER)
    if weather_data is None:
        return "Could not retrieve current weather", 502

    tz_madrid = pytz.timezone("Europe/Madrid")
    message = (
        f'Current Weather in Cercedilla🇪🇸 at '
        f'{datetime.now(tz_madrid).strftime("%Y-%m-%d %H:%M")}\n'
        f'🌡 {weather_data["metric"]["temp"]}º \n'
        f'🌧 {weather_data["metric"]["precipTotal"]} mm \n'
        f'💧 {weather_data["humidity"]} % \n'
        f'💨 {weather_data["metric"]["windSpeed"]} km/h \n'
        f'🌞 {weather_data["uv"]} UVI \nSource: {SOURCE}'
    )
    return _publish_message(message)


def parrao_weather_bot_daily(request):
    """Fetch and publish the previous day's weather through Telegram."""
    logging.info("%s Fetching daily weather...", os.getenv("ID_LOG", ""))
    tz_madrid = pytz.timezone("Europe/Madrid")
    yesterday = datetime.now(tz_madrid) - timedelta(days=1)
    day_forecast = yesterday.strftime("%Y%m%d")
    weather_data = get_api_data(URL_WEATHER_DAILY + day_forecast)
    if weather_data is None:
        return "Could not retrieve daily weather", 502

    message = (
        f'🟢 Daily summary in Cercedilla🇪🇸 ➡️ '
        f'{yesterday.strftime("%Y-%m-%d")}\n'
        f'🔴 T. Max.: {weather_data["metric"]["tempHigh"]}º \n'
        f'🔵 T. Min.: {weather_data["metric"]["tempLow"]}º \n'
        f'🌧 Precip.: {weather_data["metric"]["precipTotal"]} mm \n'
        f'💧 Humidity: {weather_data["humidityHigh"]} % - '
        f'{weather_data["humidityLow"]} %\n'
        f'💨 Max gust wind: {weather_data["metric"]["windgustHigh"]} km/h\n'
        f'⏲ Pressure: {weather_data["metric"]["pressureMax"]} hpa - '
        f'{weather_data["metric"]["pressureMin"]} hpa\n'
        f'🌞 UV high: {weather_data["uvHigh"]} UVI \n'
        f'Source: {SOURCE} '
        f'({datetime.now(tz_madrid).strftime("%Y-%m-%d %H:%M")})'
    )

    response = _publish_message(message)
    if response[1] != 200 or os.getenv("ENV_PRO", "N") != "Y":
        return response

    try:
        Weather.write_weather(weather_data)
    except Exception as err:
        logging.error("Could not save daily weather: %s", type(err).__name__)
        return "Could not save daily weather", 500
    return response


if __name__ == '__main__':

    print('***** Starting cron *****')
    parrao_weather_bot({})
    parrao_weather_bot_daily({})
    print('***** Shutdown cron *****')
