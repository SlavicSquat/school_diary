import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class U_t_L(SqlAlchemyBase):
    __tablename__ = 'users_to_lessions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    lession_id = user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("lessions.id"))
    lession = orm.relation('Lession')
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
