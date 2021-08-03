from app.crontab import crontab
from app.crontab.config import Config
from app import db
from app.health.models import Health
from sqlalchemy import delete
from datetime import datetime, timedelta

@crontab.job(minute="30", hour="0")
def clean_db():
    config = Config.read('app/crontab/config.yaml')
    if config.get('clear_db') and config.get('clear_db_days'):
        old = datetime.today() - timedelta(days=config.get('clear_db_days'))
        db.session.execute(delete(Health).where(Health.received <= old.date()))
        db.session.commit()