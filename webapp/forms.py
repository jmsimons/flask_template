#!/usr/bin/python3.8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField, BooleanField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from webapp import app
from webapp.models import User
from flask_colorpicker import colorpicker

color_picker = colorpicker(app)


class RegisterUser(FlaskForm):
    first_name = StringField('first name', validators = [DataRequired()])
    middle_name = StringField('mi', validators = [DataRequired()])
    last_name = StringField('last name', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    confirm_password = PasswordField('confirm password', validators = [DataRequired(), EqualTo('password')])
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
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
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


class InviteUser(FlaskForm):
    email = StringField('Email', validators = [Email()])
    submit = SubmitField('Send Invite')


class TableViewSelect(FlaskForm):
    table_choices = [('Email', 'email'), ('User', 'user'), ('Item', 'item'), ('Activity', 'activity')]
    table = SelectField('Select Table', choices = table_choices)
    submit = SubmitField('View Table')


class TableSearch(FlaskForm):
    value = StringField('Enter Search Term')
    submit = SubmitField('Search')


class AddVehicleForm(FlaskForm):
    year_options = list(range(1960, 2022))[::-1]
    year = SelectField('year', choices = year_options, validators = [DataRequired()])
    make = StringField('make', validators = [DataRequired()])
    model = StringField('model', validators = [DataRequired()])
    trim = StringField('trim level', validators = [DataRequired()])
    color = StringField('color')
    track_expenses = BooleanField('track expenses?')
    submit = SubmitField('Add Vehicle')


class AddCheckinForm(FlaskForm):
    type_options = ["none", "shift start", "shift end"]
    checkin_type = SelectField('type', choices = type_options, validators = [DataRequired()])
    odometer = IntegerField('odometer', validators = [DataRequired()])
    submit = SubmitField('Add Odometer Checkin')


class AddExpenseForm(FlaskForm):
    amount = FloatField('amount $', validators = [DataRequired(), NumberRange()])
    type_options = ["fuel", "maintenance", "detail", "registration", "insurance", "other"]
    expense_type = SelectField('type', choices = type_options, validators = [DataRequired()])
    interval_options = ["none", "month", "6 months", "12 months"]
    interval = SelectField('recurring?', choices = interval_options, validators = [])
    odometer = IntegerField('miles', validators = [NumberRange()])
    notes = TextAreaField("notes")
    submit = SubmitField('Add Expense')