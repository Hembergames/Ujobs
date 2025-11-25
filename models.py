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
    bio = db.Column(db.String(1000), nullable=True)
    photo = db.Column(db.String(120))

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
