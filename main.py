from flask import Flask, render_template, redirect, request, url_for
from data import db_session
import db_connection as db

HOST = 'http://127.0.0.1:8080'
app = Flask(__name__)
app.config['SECRET_KEY'] = hash('werserk_secret_key')


@app.route('/')
def hello_page():
    params = {}
    return render_template('base.html', **params)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        name = request.form['name']
        email = request.form['email']
        password = hash(request.form['password'])
        repeated_password = hash(request.form['repeated_password'])
        if db.check_email_on_registration(db_sess, email):
            return redirect(HOST + '/error?err=Email+уже+зарегистрирован')
        if password != repeated_password:
            return redirect(HOST + '/error?err=Пароли+не+совпадают')
        db.create_user(db_sess, name, email, password)
        return redirect(HOST + '/success')
    elif request.method == 'GET':
        return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        email = request.form['email']
        password = hash(request.form['password'])
        traceback = db.check_email_and_password_on_login(db_sess, email, password)
        if traceback:
            return redirect(HOST + f'/error?err={traceback}')
        return redirect(HOST + '/success')
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/error')
def error():
    if request.method == 'GET':
        params = {'err': 'Ошибка'}
        args = request.args.to_dict()
        for key in args.keys():
            params[key] = args[key]
        return render_template('success.html', traceback=params['err'])


@app.route('/success')
def success():
    params = {'traceback': 'Всё готово'}
    return render_template('success.html', **params)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
