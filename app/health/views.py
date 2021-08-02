from app import db
from app.health import bp
from app.health.models import Health
from app.catalog.models import Parkomat
from app.health.forms import DayForm
from flask import render_template, request, Response
from flask_login import login_required
from datetime import datetime
from sqlalchemy import extract, and_
import re
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.ticker import ScalarFormatter


@bp.route("/<int:host>", methods=['GET', 'POST'])
@login_required
def graph(host):
    form = DayForm()
    if form.validate_on_submit():
        year = form.year.data
        month = form.month.data
        day = form.day.data
    else:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        form.year.default = datetime.now().year
        form.month.default = datetime.now().month
        form.day.default = datetime.now().day
        form.process()
    current = db.session.query(Health).filter(Health.host==host).order_by(Health.id.desc()).first()
    return render_template("health.html", host=host, year=year, month=month, day=day, form=form, current=current)

@bp.route("/<int:host>/<int:year>/<int:month>/<int:day>/<param>.png")
def draw(host, year, month, day, param):
    preset = {
        'internet':  { 'color': 'red',   'title': 'Интернет', 'ylabel': 'Потери, %'},
        'vpn':       { 'color': 'red',   'title': 'VPN',      'ylabel': 'Потери, %'},
        'cpu':       { 'color': 'green', 'title': 'CPU',      'ylabel': 'Использовано, %'},
        'ram':       { 'color': 'green', 'title': 'RAM',      'ylabel': 'Использовано, %'},
        'hdd':       { 'color': 'green', 'title': 'HDD',      'ylabel': 'Использовано, %'},
        'usb':       { }
    }
    if param not in preset.keys():
        return Response(status=404)
    stat = db.session.query(Health).filter(and_(
                                Health.host==host,
                                extract('year', Health.received) == year,
                                extract('month', Health.received) == month,
                                extract('day', Health.received) == day)
                            ).order_by(Health.id.desc()).all()
    fig = Figure()

    if param in ('internet', 'vpn', 'cpu', 'ram', 'hdd'):
        fig.set_size_inches(w=6, h=2)
        axis = fig.add_subplot(1, 1, 1)
        xs = [s.received for s in stat]
        ys = [getattr(s, param) for s in stat]
        axis.xaxis.set_major_formatter(DateFormatter("%H:%M"))
        axis.set_ylim(ymin=0, ymax=100)
        axis.set_title(preset[param]['title'])
        axis.set_ylabel(preset[param]['ylabel'])
        axis.grid(True)
        axis.xaxis.set_major_formatter(DateFormatter("%H:%M"))
        axis.plot(xs, ys, color=preset[param]['color'])
    elif param == 'usb':
        axis_c = fig.add_subplot(4, 1, 1)
        axis_c.set(title='Монетник', ylim=[0, 1], yticks=[], xticks=[], aspect=0.02)
        axis_v = fig.add_subplot(4, 1, 2)
        axis_v.set(title='Купюрник', ylim=[0, 1], yticks=[], xticks=[], aspect=0.02)
        axis_n = fig.add_subplot(4, 1, 3)
        axis_n.set(title='NFC', ylim=[0, 1], yticks=[], xticks=[], aspect=0.02)
        axis_p = fig.add_subplot(4, 1, 4)
        axis_p.set(title='Принтер', ylim=[0, 1], yticks=[], xticks=[], aspect=0.02)
        xs = [s.received for s in stat]
        ys = [1 for s in stat if not getattr(s, 'validator')]
        axis_c.plot(xs, ys, color='red')
        axis_v.plot(xs, ys, color='red')
        axis_n.plot(xs, ys, color='red')
        axis_p.plot(xs, ys, color='red')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@bp.route("/sheet/<int:host>", methods=['GET', 'POST'])
@login_required
def sheet(host):
    form = DayForm()
    if form.validate_on_submit():
        year = form.year.data
        month = form.month.data
        day = form.day.data
    else:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        form.year.default = datetime.now().year
        form.month.default = datetime.now().month
        form.day.default = datetime.now().day
        form.process()
    health = db.session.query(Health).filter(and_(Health.host == host,
                                                  extract('year', Health.received) == year,
                                                  extract('month', Health.received) == month,
                                                  extract('day', Health.received) == day)).all()
    return render_template("health_raw.html", health=health, form=form)

@bp.route("/current")
@login_required
def current():
    health = []
    parkomats = db.session.query(Parkomat.id).filter(Parkomat.enabled==True).order_by(Parkomat.id).all()
    for p in parkomats:
        probe = db.session.query(Health).filter(Health.host==p[0]).order_by(Health.id.desc()).first()
        if probe is not None:
            health.append(probe)
    return render_template("health_current.html", health=health, parkomats=parkomats)

@bp.route("/api", methods=['POST'])
def api():
    data = request.get_json()
    host = int(re.findall(r'\d{5}', data.get('host'))[0])
    enabled = db.session.query(Parkomat.enabled).filter(Parkomat.id==host).scalar()
    if enabled:
        health = Health(
            received = datetime.now(),
            probed = data.get('time'),
            host = host,
            uptime = int(data.get('uptime')),
            internet = int(data.get('internet')),
            vpn = int(data.get('vpn')),
            cpu = int(data.get('cpu')),
            ram = int(data.get('ram')),
            hdd = int(data.get('hdd')),
            coin = data.get('usb').get('coin'),
            validator = data.get('usb').get('validator'),
            nfc = data.get('usb').get('nfc'),
            printer = data.get('usb').get('printer'),
            log = ''.join(data.get('log')),
            api = ''.join(data.get('api')),
        )
        db.session.add(health)
        db.session.commit()
    return Response(status=200)