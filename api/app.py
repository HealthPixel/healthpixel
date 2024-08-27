#!/usr/bin/python3
"""
User Profile route for the Flask Application
"""
from models import storage
from os import getenv
from flask import Flask, request, render_template, redirect, url_for, flash
from api.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

app.route('/healthpixel/')
def healthpixel():
    render_template('base.html')


if __name__ == "__main__":
    """ Main Function """
    host = getenv("HP_MYSQL_HOST")
    app.run(host=host, threaded=True, debug=True)
