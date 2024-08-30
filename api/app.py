#!/usr/bin/python3
"""
User Profile route for the Flask Application
"""
from models import storage
from os import getenv
from flask import Flask, request, render_template, redirect, url_for
from api.auth import auth
import secrets
from flask_login import LoginManager
from models.doctor import Doctor


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return storage._DBStorage__session.query(Doctor).get(id)

app.register_blueprint(auth)

@app.route('/')
def healthpixel():
    return("Hello There, your app is live!!!")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == "__main__":
    """ Main Function """
    host = getenv("HP_MYSQL_HOST", "0.0.0.0")
    app.run(host=host, port=5000, threaded=True, debug=True)
