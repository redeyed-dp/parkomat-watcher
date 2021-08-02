from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange

class AddParkomatForm(FlaskForm):
    id = IntegerField("Номер паркомата", validators=[NumberRange(min=0, max=99999)])
    submit = SubmitField("Добавить")