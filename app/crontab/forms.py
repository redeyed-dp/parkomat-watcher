from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SubmitField
from wtforms.validators import NumberRange

class CrontabForm(FlaskForm):
    clear_db = BooleanField("Автоматическое удаление данных")
    clear_db_days = IntegerField("Дней", validators=[NumberRange(min=1, max=365)])
    morning_report = BooleanField("Утренний отчет в Telegram")
    evening_report = BooleanField("Вечерний отчет в Telegram")
    submit = SubmitField("Сохранить настройки")