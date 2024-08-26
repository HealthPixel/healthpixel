#!/usr/bin/python3
"""
Creates a new User and Integrates with Backend Database
"""
from models import BaseModel, Doctor, storage
from models.base_model import Base
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('healthpixels/register', methods=['GET', 'POST'])
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

        if password != conf_password:
            flash('Passwords do not match')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = Doctor(first_name=first_name,
                          last_name=last_name,
                          phone_number=tel,
                          email=email,
                          specialization=specialization,
                          password=hashed_password)

        try:
            storage.new(new_user)
            storage.save(new_user)
            flash("User Created Successfully!!!")
            return redirect(url_for('auth.login'))
        except:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
    return (render_template('register.html'))


# @auth.route('healthpixels/login', method=['GET'])
# def login():
#     if request.method == 'GET':
#         email = request.form['email']
#         id = request.form['id']
#         password = request.form['password']

#         doctor = Doctor.query.filter_by(email=email).first()
#         if doctor and check_password_hash(doctor.password, password) and doctor.id == id:
#             login_user(doctor)
#             flash("Login Successfull")
#         else:
#                 flash('Login Unsuccessful. Please check username and password.')
#     return render_template('login.html')