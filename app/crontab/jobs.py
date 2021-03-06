from app.crontab import crontab
from app.lib.config import Config
from app.lib.telegram import alarm, tg_send_message, tg_send_file
from app import db, redis
from app.health.models import Health
from app.catalog.models import Parkomat
from sqlalchemy import delete
from datetime import datetime, timedelta

################################################################
#                      WARNING !!!                             #
# after creating new job don't forget to add it to crontab     #
#                                                              #
# cd /var/www/parkomat-watcher                                 #
# source venv/bin/activate                                     #
# flask crontab add                                            #
################################################################

@crontab.job(minute="30", hour="0")
def clean_db():
    config = Config.read()
    if config.get('clear_db') and config.get('clear_db_days'):
        old = datetime.today() - timedelta(days=config.get('clear_db_days'))
        db.session.execute(delete(Health).where(Health.received <= old.date()))
        db.session.commit()

@crontab.job(minute="55", hour="7")
def check_cert():
    config = Config.read()
    if config.get('check_cert'):
        from app.crontab.check_certificates import get_current_version, get_old_version, save_current_version
        new = get_current_version()
        if new and new > get_old_version():
            tg_send_message("‼️ <b> Доступны новые сертификаты на сайте </b><a href='https://iit.com.ua/downloads'>https://iit.com.ua/downloads</a> ‼️")
            save_current_version(new)

@crontab.job(minute="30", hour="7")
def morning():
    config = Config.read()
    if config.get('morning_report'):
        from app.reports.report import morning_report
        d = datetime.now()
        name = f"Отчет {str.zfill(str(d.day), 2)}.{str.zfill(str(d.month), 2)}.{d.year} (утро)"
        morning_report(name)
        tg_send_file(f"app/static/reports/{name}.pdf")

@crontab.job(minute="52", hour="19")
def evening_stat():
    from app.reports.report import usb_err_stat
    usb_err_stat()

@crontab.job(minute="55", hour="19")
def evening():
    config = Config.read()
    if config.get('evening_report'):
        from app.reports.report import evening_report
        d = datetime.now()
        name = f"Отчет {str.zfill(str(d.day), 2)}.{str.zfill(str(d.month), 2)}.{d.year} (вечер)"
        evening_report(name)
        tg_send_file(f"app/static/reports/{name}.pdf")

@crontab.job()
def offline_alarm():
    config = Config.read()
    if config.get('alarm_offline'):
        observed = Parkomat.observed_numbers()
        for p in observed:
            timeout = int(datetime.now().timestamp()) - redis.hget(p, 'lastmessage')
            if timeout > 15*60 and not redis.hget(p, 'offline'):
                alarm(f"⚠️ <b>Паркомат {p} оффлайн более 15 минут.</b>")
                redis.hset(p, 'offline', 1)
            elif timeout < 15*60 and redis.hget(p, 'offline'):
                alarm(f"✅ <b>Паркомат {p} теперь онлайн.</b>")
                redis.hdel(p, 'offline')
