#!/usr/bin/python3
"""
User Profile route for the Flask Application
"""
import os
from models import storage
from os import getenv
from flask import Flask, request, render_template, redirect, url_for, flash
import secrets
from flask_login import LoginManager
from models.doctor import Doctor
from models.patient import Patient
from auth import auth
from api.v1.views import app_views
from datetime import timedelta
from flask_mail import Mail, Message
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'iamgroot')

# Set the duration for the "Remember Me" cookie
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login_users'

@login_manager.user_loader
def load_user(id):
    user = storage._DBStorage__session.query(Doctor).get(id)
    if not user:
        user = storage._DBStorage__session.query(Patient).get(id)
    return user

@login_manager.unauthorized_handler
def unauthorized():
    flash('You need to be logged in to access that page.', 'error')
    # Redirect to the login page
    return redirect(url_for('auth.login_users'))

app.register_blueprint(auth)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/')
def healthpixel():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.errorhandler(403)
def unauthorzed_access(e):
    return render_template('error403.html'), 403

@app.route('/developers')
def developers():
    return render_template('developers.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = storage.query(Doctor).filter_by(email=email).first()
        if not user:
            user = storage.query(Patient).filter_by(email=email).first()

        if user:
            send_reset_email(user)
            flash('An email with instructions has been sent.', 'info')
            return redirect(url_for('auth.login_users'))
        else:
            flash('No account found with that email.', 'error')
    return render_template('forgot_password.html')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
            subject='PASSWORD RESET REQUEST',
            sender='healthpixel@gmail.com',
            recipients=[user.email])
    msg.body = f"""
    To reset your password, visit the following link:
    {url_for('reset_password', token=token, _external=True)}

    If you did not make this request, please ignore this email
    """
    mail.send(msg)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = Doctor.verify_reset_token(token) or Patient.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token!', 'error')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form.get('new_password')
        conf_password = request.form.get('conf_password')
        if password != conf_password:
            flash('Your passwords do not match!')
            return redirect(url_for('reset_password'))
        user.password = generate_password_hash(password, method='pbkdf2:sha256')
        storage.save()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login_users'))
    return render_template('reset_password.html', token=token)


if __name__ == "__main__":
    """ Main Function """
    host = getenv("HP_MYSQL_HOST", "0.0.0.0")
    app.run(host=host, port=5000, threaded=True, debug=True)
