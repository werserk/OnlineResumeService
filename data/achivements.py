import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Achivement(SqlAlchemyBase):
    __tablename__ = 'achivements'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    private = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
