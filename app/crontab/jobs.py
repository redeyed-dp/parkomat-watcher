from app.crontab import crontab
from app.crontab.config import Config
from app.crontab.telegram import tg_send_message
from app import db
from app.health.models import Health
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
    config = Config.read('app/crontab/config.yaml')
    if config.get('clear_db') and config.get('clear_db_days'):
        old = datetime.today() - timedelta(days=config.get('clear_db_days'))
        db.session.execute(delete(Health).where(Health.received <= old.date()))
        db.session.commit()

@crontab.job(minute="55", hour="7")
def check_cert():
    config = Config.read('app/crontab/config.yaml')
    if config.get('check_cert'):
        from app.crontab.check_certificates import get_current_version, get_old_version, save_current_version
        new = get_current_version()
        if new and new > get_old_version():
            tg_send_message("Доступны новые сертификаты на сайте https://iit.com.ua/downloads")
            save_current_version(new)

@crontab.job(minute="30", hour="7")
def morning():
    config = Config.read('app/crontab/config.yaml')
    if config.get('morning_report'):
        from app.crontab.report import morning_report
        morning_report()