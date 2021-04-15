from flask import Flask, render_template, redirect, request, url_for
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = hash('werserk_secret_key')


@app.route('/')
def hello_page():
    params = {}
    return render_template('base.html', **params)


@app.route('/registration', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['name'])
        print(request.form['email'])
        print(hash(request.form['password']))
        redirect('/success')
    elif request.method == 'GET':
        return render_template('registration.html')


@app.route('/success')
def success():
    params = {}
    return render_template('success.html', **params)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
