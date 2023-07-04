import os
from pathlib import PurePath, Path
from flask import Flask, request, render_template, redirect, url_for, make_response, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_ = request.form.get('USERNAME')
        password = request.form.get('PASSWORD')
        if login_ not in USERNAME:
            context={'Такого логина': login_}
            return render_template('message_login_not_found.html')
        if USERNAME == login_ and PASSWORD == password:
            return redirect(url_for('home'))
        else:
            return render_template('message_login_password_not_feet.html')
    return render_template('login.html')


@app.route('/home/')
def home():
    return render_template('index.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        mail = request.form.get('mail')
        print(name, mail)
        context = {'name': name, 'email': mail}
        return render_template('message_name.html', **context)
    return render_template('registration.html')


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
        d = c**2
        context = {'sum': c, 'square': d}
        return render_template('result.html', **context)

    return render_template('count_num.html')


@app.route('/logout')
def logout():
    return render_template('login.html')
