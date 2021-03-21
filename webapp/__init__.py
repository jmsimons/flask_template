#!/usr/bin/python3.8

import sys, os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Determine root dir #
if getattr(sys, 'frozen', False):
    root = sys._MEIPASS
else:
    root = None


# Load config #
config = {}
try:
    with open("webapp.conf") as f:
        items = [i for i in f.read().split('\n') if i != '']
        for item in items:
            k, v = item.split(':')
            if v == "False": v = False
            elif v == "True": v = True
            else:
                try: v = int(v)
                except: pass
            config[k] = v
except:
    print('Unable to load webapp.conf')


# Initialize Flask App #
if not root:
    app = Flask(__name__)
    database_filepath = 'assets/webapp.db'
else:
    template_folder = os.path.join(root, 'webapp', 'templates')
    app = Flask(__name__, template_folder=template_folder)
    database_filepath = os.path.join(root, 'webapp', 'assets', 'webapp.db')

# CORS(app)
app.config['SECRET_KEY'] = 'c-\x9b\xe9\x83\xa7\x1d\xde\x81\x982\xb5g\xd8I\x83'
if 'LOGIN_DISABLED' in config:
    app.config['LOGIN_DISABLED'] = config['LOGIN_DISABLED']
else:
    app.config['LOGIN_DISABLED'] = False


# Initialize User Database #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(database_filepath)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from webapp.db_manager import DBManager
db_manager = DBManager(db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.googleemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

try:
    with open('email.creds') as f:
        data = f.read().split('\n')
        app.config['MAIL_USERNAME'] = data[0]
        app.config['MAIL_PASSWORD'] = data[1]
        print('Email Credentials Found')
except: print('No Email Credentials Found')
    

# Imports that import objects from this script #
from webapp.routes import *
from webapp.models import User

