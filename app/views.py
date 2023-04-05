import os

from flask import request, render_template, url_for, redirect, flash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required

from . import app, db
from .models import Transactions, User
from .forms import TransactionsForm, TransactionsUpdateForm, UserRegisterForm, UserLoginForm

STATIC_ROOT = os.path.join('app', 'static')

def index():
    title = 'Данные о транзакциях'
    transaction = Transactions.query.all()
    return render_template('index.html', title=title, transaction=transaction)


def transaction_list():
    transaction_list = Transactions.query.all()
    return render_template('transaction_list.html', transaction_list=transaction_list)


def transaction_create():
    form = TransactionsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_transaction = Transactions(
                period=form.period.data,
                value=form.value.data,
                status=form.status.data,
                unit=form.unit.data,
                subject=form.subject.data
            )
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('transaction_list'))
        else:
            print(form.errors)
    return render_template('/form.html', form=form)



@login_required
def transaction_update(transaction_id):
    transaction = Transactions.query.get(transaction_id)
    form = TransactionsUpdateForm(obj=transaction)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(transaction)
            db.session.add(transaction)
            db.session.commit()
            return redirect(url_for('transaction_list'))
        else:
            print(form.errors)
    return render_template('/form.html', form=form)

@login_required
def transaction_delete(student_id):
    transaction = Transactions.query.get(student_id)
    if request.method == 'POST':
        db.session.delete(transaction)
        db.session.commit()
        return redirect(url_for('transaction_list'))
    return render_template('/transaction_delete.html', transaction=transaction)


def user_register():
    form = UserRegisterForm()
    title = 'Регистрация'
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Пользователь {new_user.username} успешно зарегестрирован', 'Успех!')
            return redirect(url_for('user_login'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При регистрации пользователя произошла ошибка{". ".join(text_list)}', 'Ошибка!')

    return render_template('accounts/index.html', form=form, title=title)


def user_login():
    form = UserLoginForm()
    title = 'Авторизация'
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно вошли в систему', 'Успех!')
                return redirect(url_for('transaction_list'))
            else:
                flash('Неверные логин и пароль', 'Ошибка!')

    return render_template('accounts/form.html', form=form, title=title)


def user_logout():
    logout_user()
    return redirect(url_for('user_login'))
