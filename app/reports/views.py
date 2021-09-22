import os
import re
from datetime import datetime
from calendar import monthrange
from app import db
from app.reports import bp
from app.reports.models import MonthReport
from app.reports.forms import MonthForm
from app.catalog.models import Parkomat
from sqlalchemy import and_, extract
from flask import render_template, flash, redirect, url_for
from flask_login import login_required

@bp.route("/")
@login_required
def archive():
    path = os.getcwd() + '/app/static/reports/'
    files = [f for f in os.listdir(path) if re.search(r'\.pdf$', f)]
    return render_template("reports_archive.html", files=files)

@bp.route("/usb/")
@login_required
def usb_index():
    return render_template("reports_usb_index.html")

@bp.route("/usb/<device>", methods=['GET', 'POST'])
@login_required
def usb(device):
    if not device in ('coin', 'validator', 'nfc', 'printer'):
        return render_template("404.html")
    form = MonthForm()
    if form.validate_on_submit():
        (year, month) = form.getMonth()
    else:
        (year, month) = form.getNow()
        form.setNow()
    days = range(1, monthrange(year, month)[1] + 1)
    drops = {}
    observed = Parkomat.observed_numbers()
    total = {}
    for p in observed:
        drops[p] = {}
        total[p] = 0
        stat = db.session.query(MonthReport).filter(and_(
                extract('year', MonthReport.date) == year,
                extract('month', MonthReport.date) == month,
                MonthReport.host == p)).all()
        for s in stat:
            drops[p][s.date.day] = getattr(s, device)
            total[p] += getattr(s, device)
    return render_template("reports_usb.html", form=form, days=days, drops=drops, total=total, device=device, sortby=form.sortby.data)
