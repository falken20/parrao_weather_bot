import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import ANY, patch

import telegram_cli
from telegram_client import TelegramDeliveryError


class TestTelegramCli(unittest.TestCase):

    @patch("telegram_cli.send_telegram_message")
    @patch("telegram_cli.load_dotenv")
    def test_sends_positional_message(self, load_dotenv, send):
        send.return_value = {"ok": True, "result": {"message_id": 42}}
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = telegram_cli.main(["Weather update"])

        self.assertEqual(exit_code, 0)
        send.assert_called_once_with("Weather update")
        load_dotenv.assert_called_once_with(ANY, override=True)
        self.assertIn("message_id=42", output.getvalue())

    @patch("telegram_cli.send_telegram_message")
    @patch("telegram_cli.load_dotenv")
    def test_reads_message_from_stdin(self, load_dotenv, send):
        send.return_value = {"ok": True, "result": {}}
        output = io.StringIO()

        stdin = io.StringIO("Line one\nLine two\n")
        with patch("telegram_cli.sys.stdin", stdin):
            with redirect_stdout(output):
                exit_code = telegram_cli.main([])

        self.assertEqual(exit_code, 0)
        send.assert_called_once_with("Line one\nLine two")
        load_dotenv.assert_called_once()

    @patch("telegram_cli.send_telegram_message")
    @patch("telegram_cli.load_dotenv")
    def test_dry_run_does_not_load_credentials_or_send(
        self, load_dotenv, send
    ):
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = telegram_cli.main(["--dry-run", "Test message"])

        self.assertEqual(exit_code, 0)
        self.assertIn("nothing was sent", output.getvalue())
        load_dotenv.assert_not_called()
        send.assert_not_called()

    @patch("telegram_cli.send_telegram_message")
    @patch("telegram_cli.load_dotenv")
    def test_returns_error_when_delivery_fails(self, load_dotenv, send):
        send.side_effect = TelegramDeliveryError(
            "Telegram rejected the message"
        )
        error_output = io.StringIO()

        with redirect_stderr(error_output):
            exit_code = telegram_cli.main(["Test message"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Telegram delivery failed", error_output.getvalue())
        load_dotenv.assert_called_once()
