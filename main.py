# by Richi Rod AKA @richionline / falken20

import os
from dotenv import load_dotenv

from src.parrao_weather_bot import parrao_weather_bot
import config_fk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Looking for .env file for environment vars
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)

SECRET_KEY = os.getenv('SECRET_KEY', default='xsd--ammmss!!"kd(sss')


if __name__ == '__main__':
    print(f'***** Starting {config_fk.SETUP_DATA["title"]} *****')
    parrao_weather_bot()
    print(f'***** Shutdown {config_fk.SETUP_DATA["title"]} *****')

