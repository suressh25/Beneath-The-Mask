from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    teamname = db.Column(db.String(100))
    ispassword = db.Column(db.Boolean)
    passwordtime = db.Column(db.String(100))
    issecurityquestion = db.Column(db.Boolean)
    securitytime = db.Column(db.String(100))
    isofa = db.Column(db.Boolean)
    completed = db.Column(db.String(100))
