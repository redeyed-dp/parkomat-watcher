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
        exists = db.session.query(Parkomat).filter(Parkomat.id == form.id.data).one()
        if exists:
            flash(f"Паркомат { form.id.data } уже есть в реестре")
            return redirect(url_for("catalog.index"))
        parkomat = Parkomat(id=form.id.data, enabled=True)
        db.session.add(parkomat)
        db.session.commit()
        flash(f"Паркомат { form.id.data } добавлен в мониторинг")
        return redirect(url_for("catalog.index"))
    parkomats = db.session.query(Parkomat).order_by(Parkomat.id).all()
    return render_template("catalog.html", parkomats=parkomats, form=form)

@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    db.session.execute(delete(Parkomat).where(Parkomat.id == id))
    db.session.execute(delete(Health).where(Health.host == id))
    db.session.commit()
    flash(f"Паркомат { id } удален")
    return redirect(url_for("catalog.index"))

@bp.route("/disable/<int:id>")
@login_required
def disable(id):
    parkomat = db.session.query(Parkomat).filter(Parkomat.id==id).one()
    parkomat.enabled = False
    db.session.commit()
    flash(f"Отключен монаторинг паркомата { id }")
    return redirect(url_for("catalog.index"))

@bp.route("/enable/<int:id>")
@login_required
def enable(id):
    parkomat = db.session.query(Parkomat).filter(Parkomat.id==id).one()
    parkomat.enabled = True
    db.session.commit()
    flash(f"Включен мониторинг паркомата { id }")
    return redirect(url_for("catalog.index"))