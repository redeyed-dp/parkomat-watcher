from app import db
from sqlalchemy import extract, and_

class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    received = db.Column(db.DateTime)
    probed = db.Column(db.DateTime)
    host = db.Column(db.Integer)
    uptime = db.Column(db.Integer)
    # System health in percents
    internet = db.Column(db.Integer)
    vpn = db.Column(db.Integer)
    cpu = db.Column(db.Integer)
    ram = db.Column(db.Integer)
    hdd = db.Column(db.Integer)
    # USB devices availability
    coin = db.Column(db.Boolean)
    validator = db.Column(db.Boolean)
    printer = db.Column(db.Boolean)
    nfc = db.Column(db.Boolean)
    # Hardware health
#    temp1 = db.Column(db.Numeric)
#    temp2 = db.Column(db.Numeric)
#    temp3 = db.Column(db.Numeric)
#    voltage1 = db.Column(db.Numeric)
#    voltage2 = db.Column(db.Numeric)
#    voltage3 = db.Column(db.Numeric)
#    sensor1 = db.Column(db.Boolean)
#    sensor2 = db.Column(db.Boolean)
    # Text logs
    log = db.Column(db.Text)
    api = db.Column(db.Text)

    @staticmethod
    def dayStat(host, year, month, day):
        return db.session.query(Health).filter(and_(Health.host == host,
                                             extract('year', Health.received) == year,
                                             extract('month', Health.received) == month,
                                             extract('day', Health.received) == day)).all()

    @staticmethod
    def counters(health):
        # Triggers. Save previous states of devices
        t = {'coin': False, 'validator': False, 'nfc': False, 'printer': False, 'uptime': 0}
        # Counters. Increment if device changes state from True to False
        c = {'coin': 0, 'validator': 0, 'nfc': 0, 'printer': 0, 'reboot': 0}
        for i in health:
            for device in ('coin', 'validator', 'printer', 'nfc'):
                if t[device] and not getattr(i, device):
                    c[device] += 1
                t[device] = getattr(i, device)
            # And count of reboots
            if t['uptime'] > i.uptime:
                c['reboot'] += 1
            t['uptime'] = i.uptime
        return c