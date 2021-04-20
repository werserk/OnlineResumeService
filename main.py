import os
from flask import Flask, render_template, request, flash, g, session
from data import db_session, db_connection as db
from data.users import User
from dotenv import load_dotenv
from email_sending.mail_sender import send_email, create_verification_code
from tools.make_response import redirect
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from flask_openid import OpenID

app = Flask(__name__)
app.config['SECRET_KEY'] = hash('werserk_secret_key')
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.abspath('tmp'))
load_dotenv()


@lm.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.before_request
def before_request():
    g.user = current_user


@app.route('/welcome')
@app.route('/')
def welcome_page():
    return render_template('base.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        name = request.form['name']
        email = request.form['email']
        password = hash(request.form['password'])
        repeated_password = hash(request.form['repeated_password'])
        if db.check_email_on_registration(db_sess, email):
            return redirect('traceback', res='Email уже зарегистрирован')
        if password != repeated_password:
            return redirect('traceback', res='Пароли не совпадают')

        session['data'] = {'code': create_verification_code(), "name": name, "email": email,
                           "hashed_password": password}

        if send_email(email, 'Завершение регистрации на OnlineResumeService',
                      f'Код для подтверждения: {session.get("data")["code"]}'):
            return redirect('confirm_registration')
        return redirect('traceback', res='Вo время отправки письма произошла ошибка')
    elif request.method == 'GET':
        return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        email = request.form['email']
        password = hash(request.form['password'])
        traceback = db.check_email_and_password_on_login(db_sess, email, password)
        login_user(db.load_user_by_email(db_sess, email))
        if traceback:
            return redirect('traceback', res=traceback)
        return redirect('traceback', res='ok')
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/my_page')
@login_required
def my_page():
    return render_template('page.html', user=g.user)


@app.route('/confirm_registration', methods=['GET', 'POST'])
def confirm_registration():
    if request.method == 'GET':
        return render_template('confirm_registration.html')
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        code = request.form['code']
        params_for_user = session.get('data')['name'], session.get('data')['email'], session.get('data')['password']
        if code == session.get('data')['code']:
            db.commit_user(db_sess, params_for_user)
            return redirect('traceback', res='Успешно')
        return redirect('traceback', res='Неправильный код')


@app.route('/traceback')
def traceback():
    params = {'res': 'Ошибка'}
    args = request.args.to_dict()
    for key in args.keys():
        params[key] = args[key]
    return render_template('traceback.html', traceback=params['res'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
