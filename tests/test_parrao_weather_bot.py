# by Richi Rod AKA @richionline / falken20
"""
File to tests using unittest library
"""

import unittest
import os
from dotenv import load_dotenv, find_dotenv
from requests import RequestException

import parrao_weather_bot


# Load env file
load_dotenv(find_dotenv())


class TestSum(unittest.TestCase):

    def test_environment_vars(self):
        self.assertIsNotNone(os.environ.get('CONSUMER_KEY'))
        self.assertIsNotNone(os.environ.get('CONSUMER_SECRET'))
        self.assertIsNotNone(os.environ.get('ACCESS_TOKEN'))
        self.assertIsNotNone(os.environ.get('ACCESS_TOKEN_SECRET'))
        self.assertIsNotNone(os.environ.get('STATION_ID'))
        self.assertIsNotNone(os.environ.get('API_KEY'))

    def test_get_weather_data(self):
        # Weather station API data
        STATION_ID = os.environ.get('STATION_ID')
        API_KEY = os.environ.get('API_KEY')
        URL_WEATHER = f"https://api.weather.com/v2/pws/observations/current?stationId={STATION_ID}" \
            f"&format=json&units=m&numericPrecision=decimal" \
            f"&apiKey={API_KEY}"

        self.assertIsNotNone(parrao_weather_bot.get_weather_data(URL_WEATHER))

    def test_get_weather_data_error(self):
        self.assertIsNone(parrao_weather_bot.get_weather_data(""))

    def test_parrao_weather_bot(self):
        os.environ["ENV_PRO"] = "N"
        with self.assertLogs() as captured:
            parrao_weather_bot.parrao_weather_bot("")

        self.assertGreater(len(captured.records), 5)
        self.assertIn(parrao_weather_bot.SOURCE,
                      captured.records[len(captured.records) - 1].getMessage())

    def test_parrao_weather_bot_with_Twitter(self):
        os.environ["ENV_PRO"] = "Y"
        parrao_weather_bot.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        with self.assertLogs() as captured:
            parrao_weather_bot.parrao_weather_bot("")

        self.assertEqual(len(captured.records), 9)
        self.assertIn("Posting tweet in Tweeter",
                      captured.records[7].getMessage())
        self.assertIn(parrao_weather_bot.SOURCE,
                      captured.records[len(captured.records) - 1].getMessage())

    def test_parrao_weather_bot_no_credentials(self):
        parrao_weather_bot.ACCESS_TOKEN = ""
        self.assertRaises(RequestException,
                          parrao_weather_bot.parrao_weather_bot, "")

    def test_parrao_weather_bot_daily(self):
        os.environ["ENV_PRO"] = "N"
        with self.assertLogs() as captured:
            parrao_weather_bot.parrao_weather_bot_daily("")

        self.assertGreater(len(captured.records), 5)
        self.assertIn(parrao_weather_bot.SOURCE,
                      captured.records[len(captured.records) - 1].getMessage())

    def test_parrao_weather_bot_daily_with_Twitter(self):
        os.environ["ENV_PRO"] = "Y"
        parrao_weather_bot.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        with self.assertLogs() as captured:
            parrao_weather_bot.parrao_weather_bot_daily("")

        self.assertEqual(len(captured.records), 9)
        self.assertIn("Posting tweet in Tweeter",
                      captured.records[7].getMessage())
        self.assertIn(parrao_weather_bot.SOURCE,
                      captured.records[len(captured.records) - 1].getMessage())

    def test_parrao_weather_bot_daily_no_credentials(self):
        parrao_weather_bot.ACCESS_TOKEN = ""
        self.assertRaises(RequestException,
                          parrao_weather_bot.parrao_weather_bot_daily, "")


if __name__ == '__main__':
    unittest.main()
