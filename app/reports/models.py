from app import db

class MonthReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.Integer)
    date = db.Column(db.Date)
    coin = db.Column(db.Integer)
    validator = db.Column(db.Integer)
    nfc = db.Column(db.Integer)
    printer = db.Column(db.Integer)