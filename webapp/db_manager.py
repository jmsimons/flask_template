#!/usr/bin/python3.8

from contextlib import contextmanager
from flask_login import login_user, current_user, logout_user, login_required
from webapp.models import User, AdminInvite, Vehicle, OdometerRecord, ShiftMilesRecord, ExpenseRecord

class DBManager:

    def __init__(self, flask_db):
        self.db = flask_db
    
    @contextmanager
    def session(self):
        s = self.db.session
        try:
            yield s
        finally:
            s.commit()
            s.close()
    
    def add_user(self, **kwargs):
        if AdminInvite.query.filter_by(email = kwargs["email"]).first():
            kwargs["admin"] = 2
        user = User(**kwargs)
        with self.session() as s:
            s.add(user)
        return True
    
    def get_user(self, **kwargs):
        user = User.query.filter_by(**kwargs).first()
        return user.get_dict()
    
    def get_user_id(self, public_id):
        user = User.query.filter_by(public_id = public_id).first()
        return user.id
    
    def get_users(self, **kwargs):
        users = User.query.filter_by(**kwargs).all()
        return [i.get_dict() for i in users]
    
    def add_admin_invite(self, email):
        invite = AdminInvite(email = email)
        with self.session() as s:
            s.add(invite)
        return True

    def add_vehicle(self, **kwargs):
        vehicle = Vehicle(**kwargs)
        with self.session() as s:
            s.add(vehicle)
        return True
    
    def get_vehicle(self, **kwargs):
        vehicle = User.query.filter_by(**kwargs).first()
        return vehicle.get_dict()
    
    def get_user_vehicles(self, **kwargs):
        vehicles = Vehicle.query.filter_by(**kwargs).all()
        miles = [self.get_vehicle_miles(i) for i in vehicles]
        vehicles = [i.get_dict() for i in vehicles]
        for i in range(len(vehicles)):
            vehicles[i].update(miles[i])
        return vehicles
    
    def get_vehicle_miles(self, vehicle_obj):
        last_checkin = OdometerRecord.query.filter_by(vehicle_id = vehicle_obj.id).order_by(OdometerRecord.id.desc()).first()
        if last_checkin:
            last_checkin = last_checkin.get_dict()
            first_checkin = OdometerRecord.query.filter_by(vehicle_id = vehicle_obj.id).first().get_dict()
            year_miles = last_checkin["odometer"] - first_checkin["odometer"]
        else:
            last_checkin, year_miles = 0, 0
        return {"last_checkin": last_checkin, "year_miles": year_miles}

    def add_checkin(self, **kwargs):
        vehicle = Vehicle.query.filter_by(public_id = kwargs['vehicle_id']).first()
        kwargs['vehicle_id'] = vehicle.id
        checkin = OdometerRecord(**kwargs)
        with self.session() as s:
            s.add(checkin)
            s.commit()
            return checkin.id, vehicle.get_dict()
    
    def start_shift_miles(self, user_id, checkin_id):
        shift = ShiftMilesRecord(**{"user_id": user_id, "odometer_start_id": checkin_id})
        with self.session() as s:
            s.add(shift)
        return True
    
    def complete_shift_miles(self, checkin_id):
        with self.session():
            shift = ShiftMilesRecord.query.order_by(ShiftMilesRecord.id.desc()).first()
            shift.odometer_end_id = checkin_id
        return True
    
    def add_expense(self, **kwargs):
        expense = ExpenseRecord(**kwargs)
        with self.session() as s:
            s.add(expense)
        return True

    def get_vehicle_expenses(self, vehicle_id):
        expenses = ExpenseRecord.query.filter_by(vehicle_id = vehicle_id).all()
        return [i.get_dict() for i in expenses]

    def get_user_expense_miles(self, user_id):
        shifts = ShiftMilesRecord.query.filter_by(user_id = user_id).all()
        return sum([i.get_miles() for i in shifts])
    