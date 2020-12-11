from . import db, SQLBase


class User(SQLBase):
    __repr_attrs__ = ['name']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
