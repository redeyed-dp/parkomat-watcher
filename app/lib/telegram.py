from app import app
import requests
from datetime import datetime

def tg_send_message(message):
    requests.get(f"https://api.telegram.org/bot{app.config['TELEGRAM_TOKEN']}/sendMessage",
        params = {
            'parse_mode': 'html',
            'chat_id': app.config['TELEGRAM_CHAT_ID'],
            'text': message
        }
    )

def tg_send_file(file):
    requests.post(f"https://api.telegram.org/bot{app.config['TELEGRAM_TOKEN']}/sendDocument",
        params = {'chat_id': app.config['TELEGRAM_CHAT_ID']},
        files = {'document': open(file, 'rb')}
    )

def alarm(message):
    now = datetime.now()
    start = now.replace(hour=8, minute=10, second=0)
    stop = now.replace(hour=19, minute=50, second=0)
    if now > start and now < stop:
        tg_send_message(message)
