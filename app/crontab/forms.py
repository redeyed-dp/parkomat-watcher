from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SubmitField
from wtforms.validators import NumberRange

class CrontabForm(FlaskForm):
    clear_db = BooleanField("Автоматическое удаление данных")
    clear_db_days = IntegerField("Дней", validators=[NumberRange(min=1, max=365)])
    morning_report = BooleanField("Утренний отчет в Telegram")
    evening_report = BooleanField("Вечерний отчет в Telegram")
    check_cert = BooleanField("Проверять обновление сертификатов на сайте https://iit.com.ua/downloads")
    alarm_hdd = BooleanField("Переполнение или отключение USB HDD")
    alarm_offline = BooleanField("Пропадание связи (оффлайн)")
    alarm_usb = BooleanField("Проблемы с USB устройствами")
    submit = SubmitField("Сохранить настройки")