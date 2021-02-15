#!/usr/bin/python3.5

import os
from webapp import app

def setup_webapp_db(): # TODO: Move this function into setup
    from webapp import db, bcrypt, User
    # from webapp.models import User, Project
    print('Building webapp database...')
    hashed_password = bcrypt.generate_password_hash("flask").decode('utf-8')
    db.create_all()
    db.session.add(User(username = "admin", email = "admin@email.com", password = hashed_password))
    db.session.commit()
    db.session.close()

if __name__ == '__main__':
    if os.path.exists('webapp/assets/webapp.db'): # TODO: remove after moving db_setup into setup routine
        print("No database detected")
        # setup_webapp_db()
    print('Webapp running with PID:', os.getpid())
    app.run(debug = True, host = '0.0.0.0', port = 5000)
