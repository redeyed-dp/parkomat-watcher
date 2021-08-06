from app.crontab import bp
from app.lib.config import Config
from app.crontab.forms import CrontabForm
from flask import render_template, redirect, url_for, flash
from flask_login import login_required

@bp.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form = CrontabForm()
    config = Config.read()
    if form.validate_on_submit():
        config['clear_db'] = form.clear_db.data
        config['clear_db_days'] = form.clear_db_days.data
        config['morning_report'] = form.morning_report.data
        config['evening_report'] = form.evening_report.data
        config['check_cert'] = form.check_cert.data
        Config.write(config)
        flash("Настройки сохранены")
        return redirect(url_for('cron.index'))
    form.clear_db.data = config.get('clear_db')
    form.clear_db_days.data = config.get('clear_db_days')
    form.morning_report.data = config.get('morning_report')
    form.evening_report.data = config.get('evening_report')
    form.check_cert.data = config.get('check_cert')
    return render_template("crontab.html", form=form)