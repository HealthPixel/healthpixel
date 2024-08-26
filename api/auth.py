#!/usr/bin/python3
"""
Creates a new User and Integrates with Backend Database
"""
from models import BaseModel, Doctor, Patient, storage
from models.base_model import Base
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash



auth = Blueprint('auth', __name__)


@auth.route('healthpixels/register', methods=['GET'])
def register():
    hashed_password = ''
    if request.method == "GET":
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        tel = request.form['tel']
        specialization = request.form['spec']
        password = request.form['password']
        conf_password = request.form['conf_password']

        if (password == conf_password):
            hashed_password = generate_password_hash(password, method='sha256')

        new_user = Doctor(first_name=first_name, last_name=last_name,
                          phone_number=tel, email=email,
                          specialization=specialization,
                          hashed_password=password)

        try:
            storage.new(new_user)
            storage.save(new_user)
            flash("User Created Successfully!!!")
        except:
            flash('Username already exists')
            return redirect(url_for('register'))
    return (render_template('signup.html'))


@auth.route('healthpixels/login', method=['GET'])
def login():
    email = request.form['email']
    id = request.form['id']
    password = request.form['password']

    doctor = Doctor.