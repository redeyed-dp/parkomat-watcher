from app import db

class Parkomat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enabled = db.Column(db.Boolean)

    @staticmethod
    def observed():
        parkomats = db.session.query(Parkomat.id).filter(Parkomat.enabled == True).order_by(Parkomat.id).all()
        numbers = [p[0] for p in parkomats]
        return numbers