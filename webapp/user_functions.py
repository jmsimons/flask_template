from flask import url_for
from flask_mail import Message
from webapp import login_manager, mail, db_manager
from webapp.models import User

# User-management functions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset Request', sender = 'noreply@webapp.i', recipients = [user.email])
    body = 'To reset your password, visit the following link:\n{}\n\nIf you did not make this request then simply ignore this email and no change will be made.\n'
    message.body = body.format(url_for('reset_token', token = token, _external = True))
    mail.send(message)

def send_admin_invite(name, email):
    token = db_manager.add_admin_invite()
    message = Message('Admin Invite Notice', sender = 'noreply@webapp.i', recipients = [email])
    body = "Hello {} You've been invited to become an admin! To sign up, visit the following link:\n{}\n\nIf you suspect that you have recieved this message in error, please ignore it.\n"
    message.body = body.format(name, url_for('register_user', token = token, _external = True))
    mail.send(message)