#!/usr/bin/python3
"""
User Profile route for the Flask Application
"""
from models import storage
from os import getenv
from flask import Flask, request, render_template, redirect, url_for, flash
from api.auth import auth
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.register_blueprint(auth)

@app.route('/')
def healthpixel():
    return("Hello There, your app is live!!!")


if __name__ == "__main__":
    """ Main Function """
    host = getenv("HP_MYSQL_HOST", "0.0.0.0")
    app.run(host=host, port=5000, threaded=True, debug=True)
