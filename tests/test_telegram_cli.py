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
    def test_accepts_message_at_length_limit(self, load_dotenv, send):
        message = "a" * 4096
        send.return_value = {"ok": True, "result": {"message_id": 42}}
        with redirect_stdout(io.StringIO()):
            exit_code = telegram_cli.main([message])

        self.assertEqual(exit_code, 0)
        load_dotenv.assert_called_once()
        send.assert_called_once_with(message)

    @patch("telegram_cli.send_telegram_message")
    @patch("telegram_cli.load_dotenv")
    def test_rejects_oversized_argument(self, load_dotenv, send):
        for options in ([], ["--dry-run"]):
            with self.subTest(options=options):
                error_output = io.StringIO()
                with redirect_stderr(error_output):
                    with self.assertRaises(SystemExit) as raised:
                        telegram_cli.main(options + ["a" * 4097])

                self.assertEqual(raised.exception.code, 2)
                self.assertIn("4096 characters", error_output.getvalue())
        load_dotenv.assert_not_called()
        send.assert_not_called()

    @patch("telegram_cli.send_telegram_message")
    @patch("telegram_cli.load_dotenv")
    def test_rejects_oversized_stdin(self, load_dotenv, send):
        with patch("telegram_cli.sys.stdin", io.StringIO("a" * 4097)):
            with redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    telegram_cli.main([])

        self.assertEqual(raised.exception.code, 2)
        load_dotenv.assert_not_called()
        send.assert_not_called()

    @patch("telegram_cli.send_telegram_message")
    @patch("telegram_cli.load_dotenv")
    def test_rejects_empty_messages(self, load_dotenv, send):
        for message in ("", " \n\t"):
            with self.subTest(message=message):
                with redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        telegram_cli.main([message])
                self.assertEqual(raised.exception.code, 2)

        with patch("telegram_cli.sys.stdin", io.StringIO(" \n\t")):
            with redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    telegram_cli.main([])
        self.assertEqual(raised.exception.code, 2)
        load_dotenv.assert_not_called()
        send.assert_not_called()

    @patch("telegram_cli.send_telegram_message")
    @patch("telegram_cli.load_dotenv")
    def test_requires_input_in_terminal(self, load_dotenv, send):
        with patch("telegram_cli.sys.stdin") as stdin:
            stdin.isatty.return_value = True
            with redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    telegram_cli.main([])
            stdin.read.assert_not_called()

        self.assertEqual(raised.exception.code, 2)
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
