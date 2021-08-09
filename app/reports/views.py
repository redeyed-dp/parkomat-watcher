import os
import re
from datetime import datetime
from app.reports import bp
from flask import render_template, flash, redirect, url_for
from flask_login import login_required

@bp.route("/")
@login_required
def archive():
    path = os.getcwd() + '/app/static/reports/'
    files = [f for f in os.listdir(path) if re.search(r'\.pdf$', f)]
    return render_template("reports_archive.html", files=files)

@bp.route("/donow/<report>")
@login_required
def donow(report):
    d = datetime.now()
    name = f"Отчет {d.year}.{str.zfill(str(d.month), 2)}.{str.zfill(str(d.day), 2)}.{str.zfill(str(d.hour), 2)}:{str.zfill(str(d.minute), 2)}"
    if report == 'evening':
        from app.reports.report import evening_report
        name += ' (вечерний)'
        evening_report(name)
    if report == 'morning':
        from app.reports.report import morning_report
        name += ' (утренний)'
        morning_report(name)
    flash(f"{name} сформирован")
    return redirect(url_for("cron.index"))