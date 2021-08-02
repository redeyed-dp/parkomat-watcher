from flask import Blueprint

bp = Blueprint('health', __name__, template_folder='templates')

from app.health import views