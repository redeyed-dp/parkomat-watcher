from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
bootstrap = Bootstrap(app)

from app.crontab import crontab
crontab.init_app(app)

from app.crontab import bp as cron
app.register_blueprint(cron, url_prefix='/cron')

from app.catalog import bp as catalog
app.register_blueprint(catalog, url_prefix='/catalog')

from app.health import bp as health
app.register_blueprint(health, url_prefix='/health')

from app.reports import bp as reports
app.register_blueprint(reports, url_prefix='/reports')

from app import views
