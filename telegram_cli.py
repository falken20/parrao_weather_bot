import argparse
import sys

from dotenv import find_dotenv, load_dotenv

from telegram_client import TelegramDeliveryError, send_telegram_message


MAX_MESSAGE_LENGTH = 4096


def build_parser():
    parser = argparse.ArgumentParser(
        description="Send a message to the configured Telegram chat."
    )
    parser.add_argument(
        "message",
        nargs="?",
        help="Message text. If omitted, read it from standard input.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the message without sending it.",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    message = args.message

    if message is None:
        if sys.stdin.isatty():
            parser.error("provide a message or pipe text through stdin")
        message = sys.stdin.read()

    message = message.strip()
    if not message:
        parser.error("message cannot be empty")
    if len(message) > MAX_MESSAGE_LENGTH:
        parser.error(
            f"message cannot exceed {MAX_MESSAGE_LENGTH} characters"
        )

    if args.dry_run:
        print("Dry run: message validated; nothing was sent.")
        return 0

    load_dotenv(find_dotenv(), override=True)
    try:
        result = send_telegram_message(message)
    except TelegramDeliveryError as err:
        print(f"Telegram delivery failed: {err}", file=sys.stderr)
        return 1

    message_id = result.get("result", {}).get("message_id")
    if message_id is None:
        print("Telegram message sent.")
    else:
        print(f"Telegram message sent (message_id={message_id}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
