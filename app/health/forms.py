from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from datetime import datetime

monthes = {
    1: 'январь',
    2: 'февраль',
    3: 'март',
    4: 'апрель',
    5: 'май',
    6: 'июнь',
    7: 'июль',
    8: 'август',
    9: 'сентябрь',
    10: 'октябрь',
    11: 'ноябрь',
    12: 'декабрь'
}

class DayForm(FlaskForm):
    year = SelectField("Год", choices=['2021'], coerce=int)
    month = SelectField("Месяц", choices=[ (i, monthes[i]) for i in monthes.keys() ], coerce=int)
    day = SelectField("День", choices=[(i, i) for i in range(1,32) ], coerce=int)
    submit = SubmitField("Показать")

    def getDay(self):
        year = self.year.data
        month = self.month.data
        day = self.day.data
        return (year, month, day)

    def getNow(self):
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        return (year, month, day)

    def setNow(self):
        self.year.default = datetime.now().year
        self.month.default = datetime.now().month
        self.day.default = datetime.now().day
        self.process()