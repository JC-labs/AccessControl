from datetime import datetime

from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

ROLE_ADMIN = 0
ROLE_USER = 1


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Logs', backref='user', lazy='dynamic')
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(64))
    action = db.Column(db.String(140))

    def __repr__(self):
        return '<Action: {}>'.format(self.action)
