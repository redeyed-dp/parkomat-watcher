from app import db
from app.catalog import bp
from app.catalog.models import Parkomat
from app.catalog.forms import AddParkomatForm
from app.health.models import Health
from sqlalchemy import delete
from flask import render_template, redirect, url_for, flash
from flask_login import login_required

@bp.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form = AddParkomatForm()
    if form.validate_on_submit():
        parkomat = Parkomat(id=form.id.data, enabled=True)
        db.session.add(parkomat)
        db.session.commit()
        flash("Паркомат {} добавлен в мониторинг".format(form.id.data))
        return redirect(url_for("catalog.index"))
    parkomats = db.session.query(Parkomat).order_by(Parkomat.id).all()
    return render_template("catalog.html", parkomats=parkomats, form=form)

@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    db.session.execute(delete(Parkomat).where(Parkomat.id == id))
    db.session.execute(delete(Health).where(Health.host == id))
    db.session.commit()
    flash("Паркомат {} удален".format(id))
    return redirect(url_for("catalog.index"))

@bp.route("/disable/<int:id>")
@login_required
def disable(id):
    parkomat = db.session.query(Parkomat).filter(Parkomat.id==id).one()
    parkomat.enabled = False
    db.session.commit()
    flash("Отключен монаторинг паркомата {}".format(id))
    return redirect(url_for("catalog.index"))

@bp.route("/enable/<int:id>")
@login_required
def enable(id):
    parkomat = db.session.query(Parkomat).filter(Parkomat.id==id).one()
    parkomat.enabled = True
    db.session.commit()
    flash("Включен мониторинг паркомата {}".format(id))
    return redirect(url_for("catalog.index"))