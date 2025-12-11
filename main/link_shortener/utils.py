import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def generate_code():
    return str(random.randint(1000, 9999))

def send_code_to_group(code, phone):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    msg = f"Код для номера {phone}: {code}"

    r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

    return r.status_code == 200
