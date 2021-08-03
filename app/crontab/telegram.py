from app import app
import requests

def tg_send_message(message):
    requests.get("https://api.telegram.org/bot{}/sendMessage".format(app.config['TELEGRAM_TOKEN']),
        params=dict(
            chat_id=app.config['TELEGRAM_CHAT_ID'],
            text=message
        )
    )