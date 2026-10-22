import os

import requests


class TelegramDeliveryError(Exception):
    pass


def send_telegram_message(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id or "<" in chat_id:
        raise TelegramDeliveryError("Telegram credentials are not configured")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(
            url,
            json={"chat_id": chat_id, "text": text},
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as err:
        status_code = getattr(
            getattr(err, "response", None), "status_code", None
        )
        detail = f" (HTTP {status_code})" if status_code else ""
        raise TelegramDeliveryError(
            f"Telegram request failed{detail}"
        ) from None
    except ValueError:
        raise TelegramDeliveryError(
            "Telegram returned an invalid response"
        ) from None

    if not isinstance(result, dict) or not result.get("ok"):
        raise TelegramDeliveryError("Telegram rejected the message")
    return result
