import os
import re
from app.reports import bp
from flask import render_template
from flask_login import login_required

@bp.route("/")
@login_required
def archive():
    path = os.getcwd() + '/app/static/reports/'
    files = [f for f in os.listdir(path) if re.search(r'\.pdf$', f)]
    return render_template("reports_archive.html", files=files)