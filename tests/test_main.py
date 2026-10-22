# by Richi Rod AKA @richionline / falken20
"""
File to tests using unittest library
"""

import unittest
import os
from unittest.mock import patch
from dotenv import load_dotenv, find_dotenv

import main
from telegram_client import send_telegram_message


# Load env file
load_dotenv(find_dotenv())


class TestParraoWeatherBot(unittest.TestCase):

    def test_environment_vars(self):
        self.assertTrue(os.environ.get('TELEGRAM_BOT_TOKEN'))
        self.assertTrue(os.environ.get('TELEGRAM_CHAT_ID'))
        self.assertIsNotNone(os.environ.get('STATION_ID'))
        self.assertIsNotNone(os.environ.get('API_KEY'))

    def test_get_weather_data(self):
        # Weather station API data
        STATION_ID = os.environ.get('STATION_ID')
        API_KEY = os.environ.get('API_KEY')
        URL_WEATHER = (
            "https://api.weather.com/v2/pws/observations/current?"
            f"stationId={STATION_ID}&format=json&units=m&"
            "numericPrecision=decimal"
            f"&apiKey={API_KEY}"
        )

        self.assertIsNotNone(main.get_api_data(URL_WEATHER))

    def test_get_weather_data_error(self):
        self.assertIsNone(main.get_api_data(""))

    def test_send_telegram_message_uses_configured_channel(self):
        with patch("telegram_client.requests.post") as post:
            post.return_value.json.return_value = {"ok": True}
            send_telegram_message("Weather update")

        self.assertEqual(
            post.call_args.kwargs["json"],
            {"chat_id": "-1001234567890", "text": "Weather update"},
        )
        self.assertEqual(post.call_args.kwargs["timeout"], 15)

    def test_parrao_weather_bot(self):
        os.environ["ENV_PRO"] = "N"
        with self.assertLogs() as captured:
            response = main.parrao_weather_bot("")

        self.assertEqual(response[1], 200)
        self.assertIn(main.SOURCE,
                      captured.records[len(captured.records) - 1].getMessage())

    def test_parrao_weather_bot_with_telegram(self):
        os.environ["ENV_PRO"] = "Y"
        with self.assertLogs() as captured:
            response = main.parrao_weather_bot("")

        self.assertEqual(response[1], 200)
        self.assertIn(main.SOURCE,
                      captured.records[len(captured.records) - 1].getMessage())

    def test_parrao_weather_bot_without_telegram_credentials(self):
        os.environ["ENV_PRO"] = "Y"
        os.environ["TELEGRAM_BOT_TOKEN"] = ""
        response = main.parrao_weather_bot("")
        self.assertEqual(response[1], 502)

    def test_parrao_weather_bot_daily(self):
        os.environ["ENV_PRO"] = "N"
        with self.assertLogs() as captured:
            response = main.parrao_weather_bot_daily("")

        self.assertEqual(response[1], 200)
        self.assertIn(main.SOURCE,
                      captured.records[len(captured.records) - 1].getMessage())

    def test_parrao_weather_bot_daily_with_telegram(self):
        os.environ["ENV_PRO"] = "Y"
        with self.assertLogs() as captured:
            response = main.parrao_weather_bot_daily("")

        self.assertEqual(response[1], 200)
        self.assertIn(main.SOURCE,
                      captured.records[len(captured.records) - 1].getMessage())

    def test_parrao_weather_bot_daily_without_telegram_credentials(self):
        os.environ["ENV_PRO"] = "Y"
        os.environ["TELEGRAM_BOT_TOKEN"] = ""
        response = main.parrao_weather_bot_daily("")
        self.assertEqual(response[1], 502)


if __name__ == '__main__':
    unittest.main()
