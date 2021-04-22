from data.users import User
from data.achivements import Achivement
from data.blobs import Blob
from werkzeug.security import check_password_hash


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


def load_user_by_id(db_sess, id):
    user = db_sess.query(User).filter(User.id == id).first()
    return user


def check_email_and_password_on_login(db_sess, email, password):
    user = db_sess.query(User).filter(User.email == email).first()
    if not user:
        return 'Пользователь+не+найден'
    if not check_password_hash(user.hashed_password, password):
        return 'Пароль+неверен'
    return 0


def create_achivement(db_sess, title, description, private, user_id):
    if db_sess.query(Achivement).filter(Achivement.title == title).first():
        return 'Достижение с таким названием уже существует'

    achivement = Achivement()
    achivement.title = title
    achivement.description = description
    achivement.private = private
    achivement.user_id = user_id

    db_sess.add(achivement)
    db_sess.commit()

    return 0


def load_achivement_by_title(db_sess, title):
    achivement = db_sess.query(Achivement).filter(Achivement.title == title).first()
    return achivement


def create_file(db_sess, blob_data, achivement_id):
    blob = Blob()
    blob.data = blob_data
    blob.achivement_id = achivement_id

    db_sess.add(blob)
    db_sess.commit()
