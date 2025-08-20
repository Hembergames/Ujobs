from db import db
from flask_login import UserMixin
from datetime import date

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, nullable=True)
    name = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    number = db.Column(db.String(15), nullable=True)
    bio = db.Column(db.String(500), nullable=True)
    photo = db.Column(db.String(120))