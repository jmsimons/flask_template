#!/usr/bin/python3.8

import time
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from webapp import app, config, db, bcrypt, send_reset_email
from webapp.models import User
from webapp.forms import RegisterUser, Login, RequestResetForm, ResetPasswordForm


### User Authentication Web Routes ###

@app.route('/register_user', methods = ['GET', 'POST'])
def register_user():
    form = RegisterUser()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
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

@app.route('/search_user')
@login_required
def search_user():
    form = SearchUser()
    return render_template('search_user.html', form = form)

@app.route('/manage_users/')
@login_required
def manage_users():
    users = User.query.all()
    return render_template('users.html', users = users)

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
    return render_template('home.html')