#!/usr/bin/python3.8

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from webapp import app, db
import time, uuid


class User(db.Model, UserMixin): ### User Project database table model ###
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.Integer)
    first = db.Column(db.String(20), nullable = False)
    middle = db.Column(db.String(20), unique = True)
    last = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    addr_street = db.Column(db.String(20))
    addr_street2 = db.Column(db.String(20))
    addr_city = db.Column(db.String(20))
    addr_state = db.Column(db.String(20))
    addr_zip = db.Column(db.String(10))
    time_stamp = db.Column(db.Integer)
    admin = db.Column(db.Integer)

    def __init__(self, **kwargs):
        kwargs["time_stamp"] = time.time()
        kwargs["public_id"] = str(uuid.uuid4())
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f"User('{self.first} {self.middle} {self.last}', '{self.email}')"

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def get_dict(self):
        return {"id": self.public_id,
                "first": self.first,
                "middle": self.middle,
                "last": self.last,
                "email": self.email,
                "street": self.addr_street,
                "street2": self.addr_street2,
                "city": self.addr_city,
                "state": self.addr_state,
                "zip": self.addr_zip,
                "admin": self.admin}

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)    


class AdminInvite(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, nullable = False)
    year = db.Column(db.String(4), nullable = False)
    make = db.Column(db.String(20), nullable = False)
    model = db.Column(db.String(20), nullable = False)
    trim = db.Column(db.String(20))
    color = db.Column(db.String(20))
    time_stamp = db.Column(db.Integer, nullable = False)
    active = db.Column(db.Boolean)
    track_expenses = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        kwargs["time_stamp"] = time.time()
        kwargs["public_id"] = str(uuid.uuid4())
        kwargs["active"] = True
        super(Vehicle, self).__init__(**kwargs)
    
    def __repr__(self):
        return f"Vehicle('{self.year}', '{self.make}', '{self.model}')"
    
    def get_dict(self):
        return {"id": self.public_id,
                "year": self.year,
                "make": self.make,
                "model": self.model,
                "trim": self.trim,
                "color": self.color,
                "time_stamp": self.time_stamp,
                "active": self.active,
                "track_expenses": self.track_expenses}


class OdometerRecord(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vehicle_id = db.Column(db.Integer, nullable = False)
    odometer = db.Column(db.Integer, nullable = False)
    time_stamp = db.Column(db.Integer, nullable = False)

    def __init__(self, **kwargs):
        kwargs["time_stamp"] = time.time()
        super(OdometerRecord, self).__init__(**kwargs)
    
    def get_dict(self):
        return {"odometer": self.odometer,
                "time_stamp": self.time_stamp}


class ShiftMilesRecord(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    odometer_start_id = db.Column(db.Integer, nullable = False)
    odometer_end_id = db.Column(db.Integer)

    def get_miles(self):
        start = OdometerRecord.query.filter_by(id = self.odometer_start_id).first().odometer
        end = OdometerRecord.query.filter_by(id = self.odometer_end_id).first().odometer
        return end - start


class ExpenseRecord(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vehicle_id = db.Column(db.Integer, nullable = False)
    odometer_id = db.Column(db.Integer)
    expense_type = db.Column(db.String(20), nullable = False)
    amount = db.Column(db.Float)
    recur_interval = db.Column(db.String(10), nullable = False)
    time_stamp = db.Column(db.Integer, nullable = False)
    notes = db.Column(db.String(512))

    def __init__(self, **kwargs):
        kwargs["time_stamp"] = time.time()
        super(ExpenseRecord, self).__init__(**kwargs)


# class PurchaseSaleRecord(db.Model):
#     id = db.Column(db.Integer, primary_key = True)


# class Reminder(db.Model):
#     id = db.Column(db.Integer, primary_key = True)