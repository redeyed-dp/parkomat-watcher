from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[InputRequired(message='Введите логин')])
    password = PasswordField('Пароль', validators=[InputRequired(message='Введите пароль')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class AdminForm(FlaskForm):
    login = StringField('Логин', validators=[Length(min=3, max=32, message='Недопустимая длина логина')])
    name = StringField('Имя', validators=[Length(min=3, max=32, message='Недопустимая длина логина')])
    password = PasswordField('Пароль', validators=[InputRequired(message='Введите пароль')])
    submit = SubmitField('Сохранить')