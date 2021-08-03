from flask_crontab import Crontab
from flask import Blueprint

crontab = Crontab()
bp = Blueprint('cron', __name__, template_folder='templates')

from app.crontab import jobs, views
