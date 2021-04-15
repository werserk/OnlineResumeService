from flask import Flask, render_template, redirect
from data import db_session
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'werserk_secret_key'


@app.route('/')
def hello_page():
    params = {}
    return render_template('base.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/success')
def success():
    params = {}
    return render_template('success.html', **params)


def main():
    # db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
