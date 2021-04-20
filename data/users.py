import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    unique_code = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    achivements = orm.relation("Achivement", back_populates='user')
