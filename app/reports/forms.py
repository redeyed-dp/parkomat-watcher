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

class MonthForm(FlaskForm):
    year = SelectField("Год", choices=['2021'], coerce=int)
    month = SelectField("Месяц", choices=[ (i, monthes[i]) for i in monthes.keys() ], coerce=int)
    submit = SubmitField("Показать")

    def getMonth(self):
        year = self.year.data
        month = self.month.data
        return (year, month)

    def getNow(self):
        year = datetime.now().year
        month = datetime.now().month
        return (year, month)

    def setNow(self):
        (year, month) = self.getNow()
        self.year.default = year
        self.month.default = month
        self.process()
