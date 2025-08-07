from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)