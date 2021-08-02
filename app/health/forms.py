from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class DayForm(FlaskForm):
    year = SelectField("Год", choices=['2021'], coerce=int)
    month = SelectField("Месяц", choices=[ (i, i) for i in range(1,13) ], coerce=int)
    day = SelectField("День", choices=[(i, i) for i in range(1,32) ], coerce=int)
    submit = SubmitField("Показать")