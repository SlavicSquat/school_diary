import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Less_in_sch(SqlAlchemyBase):
    __tablename__ = 'less_in_sch'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    klass = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    day = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    lession_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lessions.id"), nullable=True)
    place = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    lession = orm.relation('Lession')
