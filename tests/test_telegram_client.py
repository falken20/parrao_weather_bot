import unittest
from unittest.mock import Mock, patch

import requests

from telegram_client import TelegramDeliveryError, send_telegram_message

TELEGRAM_ENV = {
    "TELEGRAM_BOT_TOKEN": "unit-test-token",
    "TELEGRAM_CHAT_ID": "-10042",
}
TELEGRAM_PLACEHOLDER_ENV = {
    "TELEGRAM_BOT_TOKEN": "unit-test-token",
    "TELEGRAM_CHAT_ID": "<chat_id>",
}


class TestSendTelegramMessage(unittest.TestCase):

    @patch.dict("os.environ", TELEGRAM_ENV)
    @patch("telegram_client.requests.post")
    def test_sends_text_to_configured_chat(self, post):
        response = Mock()
        response.json.return_value = {"ok": True, "result": {"message_id": 7}}
        post.return_value = response

        result = send_telegram_message("Weather is clear")

        self.assertEqual(result["result"]["message_id"], 7)
        post.assert_called_once_with(
            "https://api.telegram.org/botunit-test-token/sendMessage",
            json={"chat_id": "-10042", "text": "Weather is clear"},
            timeout=15,
        )
        response.raise_for_status.assert_called_once_with()

    @patch.dict("os.environ", {}, clear=True)
    def test_rejects_missing_configuration(self):
        with self.assertRaisesRegex(TelegramDeliveryError, "not configured"):
            send_telegram_message("Weather is clear")

    @patch.dict("os.environ", TELEGRAM_PLACEHOLDER_ENV)
    def test_rejects_placeholder_chat_id(self):
        with self.assertRaisesRegex(TelegramDeliveryError, "not configured"):
            send_telegram_message("Weather is clear")

    @patch.dict("os.environ", TELEGRAM_ENV)
    @patch("telegram_client.requests.post")
    def test_converts_http_error_without_exposing_token(self, post):
        response = Mock(status_code=403)
        post.side_effect = requests.HTTPError("forbidden", response=response)

        with self.assertRaises(TelegramDeliveryError) as raised:
            send_telegram_message("Weather is clear")

        self.assertIn("HTTP 403", str(raised.exception))
        self.assertNotIn("unit-test-token", str(raised.exception))

    @patch.dict("os.environ", TELEGRAM_ENV)
    @patch("telegram_client.requests.post")
    def test_converts_timeout(self, post):
        post.side_effect = requests.Timeout

        with self.assertRaisesRegex(TelegramDeliveryError, "request failed"):
            send_telegram_message("Weather is clear")

    @patch.dict("os.environ", TELEGRAM_ENV)
    @patch("telegram_client.requests.post")
    def test_rejects_invalid_json(self, post):
        post.return_value.json.side_effect = ValueError("invalid JSON")

        with self.assertRaisesRegex(TelegramDeliveryError, "invalid response"):
            send_telegram_message("Weather is clear")

    @patch.dict("os.environ", TELEGRAM_ENV)
    @patch("telegram_client.requests.post")
    def test_rejects_telegram_api_error(self, post):
        post.return_value.json.return_value = {"ok": False}

        with self.assertRaisesRegex(TelegramDeliveryError, "rejected"):
            send_telegram_message("Weather is clear")

    @patch.dict("os.environ", TELEGRAM_ENV)
    @patch("telegram_client.requests.post")
    def test_rejects_unexpected_api_response_shape(self, post):
        post.return_value.json.return_value = []

        with self.assertRaisesRegex(TelegramDeliveryError, "rejected"):
            send_telegram_message("Weather is clear")
