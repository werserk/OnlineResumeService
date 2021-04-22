import sqlalchemy
from sqlalchemy import orm
from datetime import date
from .db_session import SqlAlchemyBase


class Achivement(SqlAlchemyBase):
    __tablename__ = 'achivements'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    private = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False, default=date.today())
    picture = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    user = orm.relation('User')
    achivements = orm.relation("Blob", back_populates='achivement')
