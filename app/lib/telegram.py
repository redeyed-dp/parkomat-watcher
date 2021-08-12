from app import app
import requests

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
