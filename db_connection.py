from data.users import User
from data.achivements import Achivement


def create_user(db_sess, name, email, hashed_password):
    user = User()
    user.name = name
    user.email = email
    user.hashed_password = hashed_password

    db_sess.add(user)
    db_sess.commit()


def check_email_on_registration(db_sess, email):
    was = db_sess.query(User).filter(User.email == email).first()
    return bool(was)


def check_email_and_password_on_login(db_sess, email, password):
    user = db_sess.query(User).filter(User.email == email).first()
    if not user:
        return 'Пользователь+не+найден'
    if user.hashed_password != password:
        return 'Пароль+неверен'
    return 0
