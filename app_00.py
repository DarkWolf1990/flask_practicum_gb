from pathlib import PurePath, Path
from flask import Flask, request, render_template, redirect, url_for, make_response, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '48d935e6d7bedc431ae1f101c032b1227ad2c79689df0932c93a1e3be28e9c3b'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        return redirect(url_for('home'))
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


@app.route('/three/')
def three():
    return render_template('three.html')


@app.route('/logout')
def logout():
    return render_template('login.html')
