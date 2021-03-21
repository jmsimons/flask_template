#!/usr/bin/python3.8

import time
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from webapp import app, config, db, db_manager, bcrypt
from webapp.models import User
from webapp.forms import RegisterUser, Login, RequestResetForm, ResetPasswordForm, InviteUser, TableViewSelect, TableSearch, AddVehicleForm, AddCheckinForm, AddExpenseForm
from webapp.user_functions import send_reset_email, send_admin_invite
from webapp.prepare_functions import prep_expense_summary


### User Function Web Routes ###

@app.route('/register_user', methods = ['GET', 'POST'])
@login_required
def register_user():
    form = RegisterUser()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = {"first": form.first_name.data,
                "middle": form.middle_name.data,
                "last": form.last_name.data,
                "email": form.email.data,
                "password": hashed_password}
        if db_manager.add_user(**user):
            return redirect(url_for('home'))
    return render_template('register_user.html', title = 'Register User', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password.')
    return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/manage_users', methods = ['GET', 'POST'])
@login_required
def manage_users():
    table_cols = ["first", "middle", "last", "email", "admin"]
    table_rows = None
    invite_form = InviteUser()
    search_form = TableSearch()
    if request.method == 'POST':
        if request.form.get('submit') == 'Send Invite':
            if current_user.admin >= 2:
                email = request.form.get('email')
                send_admin_invite('name', email)
                if db_manager.add_admin_invite(email):
                    flash(f'Admin invite sent to {email}', "success")
            else:
                flash('Insufficient Privileges')
        elif request.form.get('submit') == 'Search':
            key = request.form.get('criteria')
            value = request.form.get('value')
            kwarg = {key: value}
            print('Applying search term', kwarg)
            table_rows = [i.get_row() for i in User.query.filter_by(**kwarg).all() if i.level]
            if not table_rows:
                flash("Your search didn't return any results.")
    if table_rows == None:
        table_rows = db_manager.get_users()
    return render_template('admin_users.html', title = 'Manage Admin Users', invite_form = invite_form, search_form = search_form, table_cols = table_cols, table_rows = table_rows, enumerate = enumerate)

@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)

@app.route('/reset_password/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)


### Main App Web Routes ###

@app.route('/')
@login_required
def home():
    user_id = current_user.get_id()
    user = db_manager.get_user(**{"id": user_id})
    reminders = []
    expense_summary = prep_expense_summary(user_id, "2021")
    print(expense_summary)
    vehicles = db_manager.get_user_vehicles(**{"user_id": user_id})
    return render_template('home.html', user = user, reminders = reminders, expenses = expense_summary, vehicles = vehicles)

@app.route('/add_vehicle', methods = ['GET', 'POST'])
@login_required
def add_vehicle():
    uid = {"id": current_user.get_id()}
    user = db_manager.get_user(**uid)
    form = AddVehicleForm()
    if form.validate_on_submit():
        vehicle = {"user_id": uid["id"],
                   "year": form.year.data,
                   "make": form.make.data,
                   "model": form.model.data,
                   "trim": form.trim.data,
                   "color": form.color.data}
        if db_manager.add_vehicle(**vehicle):
            flash(f"You added a {vehicle['year']} {vehicle['make']} {vehicle['model']} to your garage!", "success")
        return redirect(url_for("home"))
    return render_template('add_vehicle.html', user = user, form = form)

@app.route('/add_checkin/<vehicle_id>', methods = ['GET', 'POST'])
@login_required
def add_checkin(vehicle_id):
    user = db_manager.get_user(**{"id": current_user.get_id()})
    form = AddCheckinForm()
    # vehicle = db_manager.get_vehicle(public_id = vehicle_id)
    if form.validate_on_submit():
        checkin = {"vehicle_id": vehicle_id,
                   "odometer": form.odometer.data}
        checkin_id, vehicle = db_manager.add_checkin(**checkin)
        checkin_type = form.checkin_type.data
        if checkin_type == "shift start":
            db_manager.start_shift_miles(db_manager.get_user_id(user["id"]), checkin_id)
        elif checkin_type == "shift end":
            if db_manager.complete_shift_miles(checkin_id):
                flash(f"You completed shift miles!", "success")
        flash(f"You added an odometer checkin for your {vehicle['year']} {vehicle['make']} {vehicle['model']}!", "success")
        return redirect(url_for("home"))
    return render_template('add_checkin.html', user = user, form = form)

@app.route('/add_expense/<vehicle_id>', methods = ['GET', 'POST'])
@login_required
def add_expense(vehicle_id):
    user = db_manager.get_user(**{"id": current_user.get_id()})
    form = AddExpenseForm()
    if form.validate_on_submit():
        if form.odometer.data:
            checkin = {"odometer": form.odometer.data,
                       "vehicle_id": vehicle_id}
            checkin_id, vehicle = db_manager.add_checkin(**checkin)
        else:
            checkin_id = None
        expense = {"vehicle_id": vehicle["id"],
                   "expense_type": form.expense_type.data,
                   "recur_interval": form.interval.data,
                   "notes": form.notes.data,
                   "odometer_id": checkin_id}
        if db_manager.add_expense(**expense):
            if expense["recur_interval"] == "none":
                message = f"You added a one-time {expense['expense_type']} expense!"
            else:
                message = f"You added a(n) {expense['expense_type']} expense that recurs every {expense['recur_interval']}!"
            flash(message, "success")
        return redirect(url_for("home"))
    return render_template('add_expense.html', user = user, form = form)