from app import db

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