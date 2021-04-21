import sqlalchemy
from .db_session import SqlAlchemyBase


class Lession(SqlAlchemyBase):
    __tablename__ = 'lessions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
