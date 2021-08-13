from app import db

class Parkomat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Installed devices
    coin = db.Column(db.Boolean)
    validator = db.Column(db.Boolean)
    nfc = db.Column(db.Boolean)
    # Enable monitoring
    enabled = db.Column(db.Boolean)

    @staticmethod
    def observed_numbers():
        parkomats = db.session.query(Parkomat.id).filter(Parkomat.enabled == True).order_by(Parkomat.id).all()
        numbers = [p[0] for p in parkomats]
        return numbers

    @staticmethod
    def observed():
        parkomats = db.session.query(Parkomat.id).filter(Parkomat.enabled == True).order_by(Parkomat.id).all()
        return parkomats

    @staticmethod
    def device_configs():
        devices = {}
        parkomats = db.session.query(Parkomat).filter(Parkomat.enabled == True).order_by(Parkomat.id).all()
        for parkomat in parkomats:
            devices[parkomat.id] = {}
            for dev in ('coin', 'validator', 'nfc'):
                devices[parkomat.id][dev] = getattr(parkomat, dev)
        return devices
