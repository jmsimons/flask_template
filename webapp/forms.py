#!/usr/bin/python3.8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from webapp.models import User


class RegisterUser(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 5, max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register User')


class SearchUser(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    search = SubmitField('Search')


class EditUser(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    search = SubmitField('Search')


class RemoveUser(FlaskForm):
    remove = BooleanField('Are you sure you want to permanently remove this user?')
    search = SubmitField('Remove')


class Login(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if not user:
            raise ValidationError('There is no account with that email. Contact the administrator.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')