# by Richi Rod AKA @richionline / falken20
"""
File to tests using unittest library
"""

import os
import unittest
from copy import deepcopy
from unittest.mock import Mock, patch

import requests

import main
from telegram_client import TelegramDeliveryError


CURRENT_WEATHER = {
    "metric": {"temp": 14.8, "precipTotal": 1.2, "windSpeed": 3.4},
    "humidity": 60,
    "uv": 2,
}
DAILY_WEATHER = {
    "metric": {
        "tempHigh": 20.2,
        "tempLow": 9.7,
        "precipTotal": 3.51,
        "windgustHigh": 9.3,
        "pressureMax": 1020.12,
        "pressureMin": 1017.44,
    },
    "humidityHigh": 99,
    "humidityLow": 66,
    "uvHigh": 5,
}
WEATHER_URL = "https://weather.test/current"


class TestMain(unittest.TestCase):

    def test_get_api_data_returns_first_observation(self):
        response = Mock()
        response.json.return_value = {
            "observations": [CURRENT_WEATHER, {"metric": {"temp": 99}}]
        }
        with patch("main.requests.get", return_value=response) as get:
            result = main.get_api_data(WEATHER_URL)

        self.assertEqual(result, CURRENT_WEATHER)
        get.assert_called_once_with(WEATHER_URL, timeout=15)
        response.raise_for_status.assert_called_once_with()

    def test_get_api_data_returns_none_on_timeout(self):
        with patch("main.requests.get", side_effect=requests.Timeout):
            self.assertIsNone(main.get_api_data(WEATHER_URL))

    def test_get_api_data_returns_none_on_http_error(self):
        for status_code in (400, 429, 500):
            with self.subTest(status_code=status_code):
                response = Mock(status_code=status_code)
                response.raise_for_status.side_effect = requests.HTTPError(
                    response=response
                )
                with patch("main.requests.get", return_value=response):
                    self.assertIsNone(main.get_api_data(WEATHER_URL))
                response.json.assert_not_called()

    def test_get_api_data_returns_none_on_invalid_json(self):
        response = Mock()
        response.json.side_effect = ValueError("Invalid JSON")
        with patch("main.requests.get", return_value=response):
            self.assertIsNone(main.get_api_data(WEATHER_URL))

    def test_get_api_data_returns_none_on_invalid_payload(self):
        payloads = (
            None, [], {}, "invalid", {"observations": None},
            {"observations": []}, {"observations": {}},
            {"observations": "invalid"}, {"observations": [None]},
            {"observations": [[]]}, {"observations": ["invalid"]},
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                response = Mock()
                response.json.return_value = payload
                with patch("main.requests.get", return_value=response):
                    self.assertIsNone(main.get_api_data(WEATHER_URL))

    def _assert_weather_rejected(self, handler, weather_data):
        with patch.dict(os.environ, {"ENV_PRO": "Y"}), patch(
            "main.get_api_data", return_value=weather_data
        ), patch("main.send_telegram_message") as send, patch.object(
            main.Weather, "write_weather"
        ) as save:
            result = handler({})

        self.assertEqual(result[1], 502)
        send.assert_not_called()
        save.assert_not_called()

    def test_handlers_reject_invalid_observation_shapes(self):
        invalid_observations = (
            None, [], "invalid", {}, {"metric": None}, {"metric": []},
        )
        for handler in (
            main.parrao_weather_bot, main.parrao_weather_bot_daily
        ):
            for weather_data in invalid_observations:
                with self.subTest(handler=handler.__name__, data=weather_data):
                    self._assert_weather_rejected(handler, weather_data)

    def test_handlers_reject_each_missing_required_field(self):
        for handler, template in (
            (main.parrao_weather_bot, CURRENT_WEATHER),
            (main.parrao_weather_bot_daily, DAILY_WEATHER),
        ):
            paths = [(field,) for field in template]
            paths.extend(("metric", field) for field in template["metric"])
            for path in paths:
                with self.subTest(handler=handler.__name__, field=path):
                    weather_data = deepcopy(template)
                    container = weather_data
                    if len(path) == 2:
                        container = weather_data["metric"]
                    del container[path[-1]]
                    self._assert_weather_rejected(handler, weather_data)

    def test_handlers_reject_invalid_numeric_values(self):
        invalid_values = (
            None, "20.2", "invalid", True, False, [], {},
            float("nan"), float("inf"), float("-inf"), 10 ** 400,
        )
        for handler, template in (
            (main.parrao_weather_bot, CURRENT_WEATHER),
            (main.parrao_weather_bot_daily, DAILY_WEATHER),
        ):
            paths = [(field,) for field in template if field != "metric"]
            paths.extend(("metric", field) for field in template["metric"])
            for path in paths:
                for value in invalid_values:
                    with self.subTest(
                        handler=handler.__name__, field=path, value=value
                    ):
                        weather_data = deepcopy(template)
                        container = weather_data
                        if len(path) == 2:
                            container = weather_data["metric"]
                        container[path[-1]] = value
                        self._assert_weather_rejected(handler, weather_data)

    def test_current_handler_returns_502_when_weather_is_unavailable(self):
        with patch("main.get_api_data", return_value=None), patch(
            "main.send_telegram_message"
        ) as send:
            result = main.parrao_weather_bot({})

        self.assertEqual(result, ("Could not retrieve current weather", 502))
        send.assert_not_called()

    def test_current_handler_dry_run_does_not_send(self):
        with patch.dict(os.environ, {"ENV_PRO": "N"}), patch(
            "main.get_api_data", return_value=CURRENT_WEATHER
        ), patch("main.send_telegram_message") as send:
            result = main.parrao_weather_bot({})

        self.assertEqual(result, ("Dry run; message not sent", 200))
        send.assert_not_called()

    def test_current_handler_sends_formatted_message(self):
        with patch.dict(os.environ, {"ENV_PRO": "Y"}), patch(
            "main.get_api_data", return_value=CURRENT_WEATHER
        ), patch("main.send_telegram_message") as send:
            result = main.parrao_weather_bot({})

        self.assertEqual(result, ("Message sent", 200))
        message = send.call_args.args[0]
        self.assertIn("14.8º", message)
        self.assertIn(main.SOURCE, message)

    def test_current_handler_returns_502_when_telegram_fails(self):
        with patch.dict(os.environ, {"ENV_PRO": "Y"}), patch(
            "main.get_api_data", return_value=CURRENT_WEATHER
        ), patch(
            "main.send_telegram_message",
            side_effect=TelegramDeliveryError("rejected"),
        ):
            result = main.parrao_weather_bot({})

        self.assertEqual(result, ("Telegram delivery failed", 502))

    def test_daily_handler_requests_yesterday_and_saves_after_sending(self):
        with patch.dict(os.environ, {"ENV_PRO": "Y"}), patch(
            "main.get_api_data", return_value=DAILY_WEATHER
        ) as get_weather, patch(
            "main.send_telegram_message"
        ) as send, patch.object(main.Weather, "write_weather") as save:
            result = main.parrao_weather_bot_daily({})

        self.assertEqual(result, ("Message sent", 200))
        self.assertTrue(
            get_weather.call_args.args[0].startswith(main.URL_WEATHER_DAILY)
        )
        self.assertRegex(get_weather.call_args.args[0], r"date=\d{8}$")
        self.assertIn("T. Max.: 20.2º", send.call_args.args[0])
        save.assert_called_once_with(DAILY_WEATHER)

    def test_daily_handler_returns_502_when_weather_is_unavailable(self):
        with patch.dict(os.environ, {"ENV_PRO": "Y"}), patch(
            "main.get_api_data", return_value=None
        ), patch("main.send_telegram_message") as send, patch.object(
            main.Weather, "write_weather"
        ) as save:
            result = main.parrao_weather_bot_daily({})

        self.assertEqual(result, ("Could not retrieve daily weather", 502))
        send.assert_not_called()
        save.assert_not_called()

    def test_daily_handler_does_not_save_when_telegram_fails(self):
        with patch.dict(os.environ, {"ENV_PRO": "Y"}), patch(
            "main.get_api_data", return_value=DAILY_WEATHER
        ), patch(
            "main.send_telegram_message",
            side_effect=TelegramDeliveryError("rejected"),
        ), patch.object(main.Weather, "write_weather") as save:
            result = main.parrao_weather_bot_daily({})

        self.assertEqual(result, ("Telegram delivery failed", 502))
        save.assert_not_called()

    def test_daily_handler_reports_database_failure(self):
        with patch.dict(os.environ, {"ENV_PRO": "Y"}), patch(
            "main.get_api_data", return_value=DAILY_WEATHER
        ), patch("main.send_telegram_message"), patch.object(
            main.Weather, "write_weather", side_effect=RuntimeError
        ):
            result = main.parrao_weather_bot_daily({})

        self.assertEqual(result, ("Could not save daily weather", 500))

    def test_daily_dry_run_does_not_save_to_database(self):
        with patch.dict(os.environ, {"ENV_PRO": "N"}), patch(
            "main.get_api_data", return_value=DAILY_WEATHER
        ), patch("main.send_telegram_message") as send, patch.object(
            main.Weather, "write_weather"
        ) as save:
            result = main.parrao_weather_bot_daily({})

        self.assertEqual(result, ("Dry run; message not sent", 200))
        send.assert_not_called()
        save.assert_not_called()
