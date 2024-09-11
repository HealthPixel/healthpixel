#!/usr/bin/python3
"""
User Profile route for the Flask Application
"""
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


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Set the duration for the "Remember Me" cookie
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

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
    flash('You need to log in before accessing this page.', 'error')
    # Redirect to the login page
    return redirect(url_for('auth.login_users'))

app.register_blueprint(auth)
app.register_blueprint(app_views)


@app.route('/')
def healthpixel():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.errorhandler(403)
def unauthorzed_access(e):
    return render_template('error403.html'), 403

if __name__ == "__main__":
    """ Main Function """
    host = getenv("HP_MYSQL_HOST", "0.0.0.0")
    app.run(host=host, port=5000, threaded=True, debug=True)
