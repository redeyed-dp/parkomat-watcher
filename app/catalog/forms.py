from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SubmitField
from wtforms.validators import NumberRange

class AddParkomatForm(FlaskForm):
    id = IntegerField("Номер паркомата", validators=[NumberRange(min=0, max=99999)])
    submit = SubmitField("Добавить")

class EditParkomatForm(FlaskForm):
    coin = BooleanField("Монетоприемник (USB-UART адаптер FT-340)")
    validator = BooleanField("Купюроприемник (USB-UART адаптер FTDI-2302)")
    nfc = BooleanField("NFC Excellio")
    submit = SubmitField("Сохранить")
