import requests
import os
from dotenv import load_dotenv


load_dotenv() 


def send_telegram_msg(chat_id, text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "TELEGRAM API TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Telegram error: {e}")
