from flask_wtf import FlaskForm
import wtforms as wf

from .models import Transactions, User
from . import app

class TransactionsForm(FlaskForm):
    period = wf.StringField(label='Хранение периода', validators=[
        wf.validators.DataRequired()
    ])
    value = wf.IntegerField(label='Хранение суммы', validators=[
        wf.validators.DataRequired(),
        wf.validators.NumberRange(min=0, max=100)
    ])
    status = wf.StringField(label='Хранение статуса', validators=[
        wf.validators.DataRequired()
    ])
    unit = wf.StringField(label='Хранение типа валют', validators=[
        wf.validators.DataRequired()
    ])
    subject = wf.TextAreaField(label='Хранение комментария проводки', validators=[
        wf.validators.DataRequired()
    ])


class TransactionsUpdateForm(FlaskForm):
    period = wf.StringField(label='Хранение периода', validators=[
        wf.validators.DataRequired()
    ])
    value= wf.IntegerField(label='Хранение суммы', validators=[
        wf.validators.DataRequired(),
        wf.validators.NumberRange(min=0, max=2000)
    ])
    status = wf.StringField(label='Хранение статуса', validators=[
        wf.validators.DataRequired()
    ])
    unit = wf.StringField(label='Хранение типа валют', validators=[
        wf.validators.DataRequired()
    ])
    subject = wf.DateField(label='Хранение комментария проводки', validators=[
        wf.validators.DataRequired()
    ])


class UserLoginForm(FlaskForm):
    username = wf.StringField(label='Логин', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=20)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired(),
    ])

    def validate_password(self, field):
        if len(field.data) < 8:
            raise wf.ValidationError('Длина пароля должна быть минимум 8 символов')


class UserRegisterForm(UserLoginForm):
    password2 = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired(),
    ])

    def validate(self, *args, **kwargs):
        if not super().validate(*args, **kwargs):
            return False
        if self.password.data != self.password2.data:
            self.password2.errors.append('Пароли должны совпадать')
            return False
        return True

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise wf.ValidationError('Пользователь с таким username уже существует')

