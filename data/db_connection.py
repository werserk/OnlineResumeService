from data.users import User
from data.achivements import Achivement


def create_user(name, email, hashed_password):
    user = User()
    user.name = name
    user.email = email
    user.hashed_password = hashed_password

    return user


def commit_user(db_sess, user_parametres):
    user = create_user(*user_parametres)

    db_sess.add(user)
    db_sess.commit()


def check_email_on_registration(db_sess, email):
    was = db_sess.query(User).filter(User.email == email).first()
    return bool(was)


def load_user_by_email(db_sess, email):
    user = db_sess.query(User).filter(User.email == email).first()
    return user


def check_email_and_password_on_login(db_sess, email, password):
    user = db_sess.query(User).filter(User.email == email).first()
    if not user:
        return 'Пользователь+не+найден'
    if user.hashed_password != password:
        return 'Пароль+неверен'
    return 0
