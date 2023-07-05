import os
from pathlib import PurePath, Path
from flask import Flask, request, render_template, redirect, url_for, make_response, session
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from forms_registration import RegisterForm
from forms_login import LoginForm

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
csrf = CSRFProtect(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user_name = form.user_name.data
        password = form.password.data
        print(user_name, password)
        if user_name not in USERNAME:
            context = {'Такого логина': user_name}
            return render_template('message_login_not_found.html')
        if USERNAME == user_name and PASSWORD == password:
            return redirect(url_for('home'))
        else:
            return render_template('message_login_password_not_feet.html')
    return render_template('login.html', form=form)


@app.route('/home/')
def home():
    return render_template('index.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        mail = form.mail.data
        password = form.password.data
        password2 = form.password2.data
        context = {'first_name': first_name, 'last_name': last_name, 'password': password, 'password2': password2,
                   'email': mail}
        response = make_response(render_template('message_name.html', **context))
        response.set_cookie('first_name', first_name)
        response.set_cookie('last_name', last_name)
        response.set_cookie('mail', mail)
        response.set_cookie('password', password)
        response.set_cookie('password2', password2)
        return response
    return render_template('registration.html', form=form)


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
        return render_template('donwload_message.html')

    return render_template('upload.html')


@app.route('/text_area/', methods=['GET', 'POST'])
def text_area():
    if request.method == 'POST':
        text = request.form.get('text_area')
        res = len(text.split())
        return f'{res}'
    return render_template('text_area.html')


@app.route('/count_num', methods=['GET', 'POST'])
def count_num():
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        a = int(num1)
        b = int(num2)
        c = a + b
        d = c ** 2
        context = {'sum': c, 'square': d}
        return render_template('result.html', **context)

    return render_template('count_num.html')


@app.route('/logout')
def logout():
    response = make_response(redirect('/registration/'))
    response.delete_cookie('first_name')
    response.delete_cookie('last_name')
    response.delete_cookie('mail')
    response.delete_cookie('password')
    response.delete_cookie('password2')
    return response
