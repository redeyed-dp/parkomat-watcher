from app import redis
from app.lib.telegram import alarm
from app.lib.config import Config
from datetime import datetime

def analyzer(host, data):
    config = Config.read()
    # when last message received
    redis.hset(host, 'lastmessage', int(datetime.now().timestamp()))

    # no free space on HDD or USB drive disconnected
    if config.get('alarm_hdd'):
        if data.get('hdd') == 0 and not redis.hget(host, 'hdd'):
            redis.hset(host, 'hdd', 'disconnect')
            alarm(f"⚠️ <b> Паркомат { host }. Отпадание жесткого диска.</b>")
        elif data.get('hdd') > 99 and not redis.hget(host, 'hdd'):
            redis.hset(host, 'hdd', 'full')
            alarm(f"⚠️ <b> Паркомат { host }. Жесткий диск заполнен на {data.get('hdd')}% </b>")
        elif data.get('hdd') > 0 and data.get('hdd') < 99 and redis.hget(host, 'hdd'):
            redis.hdel(host, 'hdd')
            alarm(f"✅ Паркомат { host }. Проблема с жестким диском устранена.")

    # Coin USB port
    if not data.get('usb').get('coin'):
        if not redis.hget(host, 'coin'):
            redis.hset(host, 'coin', 1)
        else:
            c = int(redis.hget(host, 'coin'))
            redis.hset(host, 'coin', c+1)
        if int(redis.hget(host, 'coin')) == 15 and config.get('alarm_usb'):
            alarm(f"⚠️ Паркомат { host }. Отпал монетоприемник.")
    elif redis.hget(host, 'coin'):
        if int(redis.hget(host, 'coin')) >= 15 and config.get('alarm_usb'):
            alarm(f"✅ Паркомат { host }. Монетоприемник подключен.")
        redis.hdel(host, 'coin')

    # Validator USB port
    if not data.get('usb').get('validator'):
        if not redis.hget(host, 'validator'):
            redis.hset(host, 'validator', 1)
        else:
            v = int(redis.hget(host, 'validator'))
            redis.hset(host, 'validator', v+1)
        if int(redis.hget(host, 'validator')) == 15 and config.get('alarm_usb'):
            alarm(f"⚠️ Паркомат { host }. Отпал купюроприемник.")
    elif redis.hget(host, 'validator'):
        if int(redis.hget(host, 'validator')) >= 15 and config.get('alarm_usb'):
            alarm(f"✅ Паркомат { host }. Купюроприемник подключен.")
        redis.hdel(host, 'validator')
