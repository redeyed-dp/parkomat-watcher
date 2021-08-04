from app import db
from app.catalog.models import Parkomat
from app.health.models import Health
from app.crontab.telegram import tg_send_message
from sqlalchemy import and_
from datetime import datetime, timedelta

def morning_report():
    offline = []
    api = []
    parkomats = Parkomat.observed()
    old = datetime.today() - timedelta(minutes=30)
    for p in parkomats:
        count = db.session.query(Health).filter(and_(Health.host == p, Health.received > old)).count()
        if count == 0:
            offline.append(p)
        else:
            lastprobe = db.session.query(Health.api).filter(Health.host == p).order_by(Health.id.desc()).first()
            if lastprobe.api != 'ok':
                api.append("№{}: {}\n".format(p, lastprobe.api))
    if len(offline) > 0:
        tg_send_message("Не вышли на связь: {}".format(', '.join(offline)))
    if len(api) > 0:
        tg_send_message("Проблемы API: \n {}".format("\n".join(api)))
    if len(offline) == 0 and len(api) == 0:
        tg_send_message("На всех наблюдаемых паркоматах все ОК :-)")