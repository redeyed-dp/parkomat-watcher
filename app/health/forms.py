from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

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