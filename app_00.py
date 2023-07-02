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
            return f' login {login_} not found!'
        if USERNAME == login_ and PASSWORD == password:
            return redirect(url_for('home'))
        else:
            return f'login and password not complete!'
    return render_template('login.html')


@app.route('/home/')
def home():
    return render_template('index.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
        return render_template('donwload_message.html')

    return render_template('upload.html')


@app.route('/text_area/')
def text_area():
    return render_template('text_area.html')


@app.route('/logout')
def logout():
    return render_template('login.html')
