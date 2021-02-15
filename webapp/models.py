#!/usr/bin/python3.8

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from webapp import app, db
import time


class User(db.Model, UserMixin): ### User Project database table model ###
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    admin = db.Column(db.Boolean)

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "User('{}', '{}')".format(self.username, self.email)