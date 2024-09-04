#!/usr/bin/python3
"""
Creates a new User and Integrates with Backend Database
"""
from models import storage
from models.doctor import Doctor
from models.patient import Patient
from models.base_model import Base, BaseModel
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    errors = []
    error_empty_fields = ''
    error_pwd_mismatch = ''
    if request.method == "POST":
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        tel = request.form['tel']
        specialization = request.form['spec']
        password = request.form['password']
        conf_password = request.form['conf_password']

        # Check if all fields are not empty
        if not first_name or not last_name or not email or not tel or not specialization or not password or not conf_password:
            error_empty_fields = 'All fields are required'
            errors.append(error_empty_fields)

        doctor = storage._DBStorage__session.query(Doctor).filter_by(email=email).first()

        if doctor:
            error_reg_user = 'User already exist, use a different email!'
            errors.append(error_reg_user)
            return render_template('register.html', err_reg_user=error_reg_user)

        # Check if passwords match before hashing
        if password != conf_password:
            error_pwd_mismatch = 'Passwords do not match'
            errors.append(error_pwd_mismatch)
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if not errors:
            new_doc = Doctor(first_name=first_name,
                            last_name=last_name,
                            phone_number=tel,
                            email=email,
                            specialization=specialization,
                            password=hashed_password)

            try:
                storage.new(new_doc)
                storage.save()
                # register_success = "You have successfully created an account. Please log in!"
                if not errors:
                    login_user(new_doc)
                    return redirect(url_for('auth.dashboard', id=new_doc.id))
            except Exception as e:
                errors.append(f'Error: {str(e)}')
    return render_template('register.html',
                           error_ef = error_empty_fields,
                           error_pm = error_pwd_mismatch)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    del_success = request.args.get('del_success')
    errors = []
    error_login = ''
    error_empty_fields = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form
        
        # Check if all fields are not empty
        if not email or not password:
            error_empty_fields = 'All fields are required'
            errors.append(error_empty_fields)
            return render_template('login.html', err_ef=error_empty_fields)

        # Try to find the user in Doctor model
        user = storage._DBStorage__session.query(Doctor).filter_by(email=email).first()

        # If not found, try to find the user in Patient model
        if not user:
            user = storage._DBStorage__session.query(Patient).filter_by(email=email).first()

        # Validate password
        if not (user and check_password_hash(user.password, password)):
            error_login = 'Invalid Login. Check Username or Password!'
            errors.append(error_login)
            return render_template('login.html', err_login=error_login)

        if not errors:
            login_user(user, remember=remember)

            # Redirect based on the user role(Doctor or Patient)
            if isinstance(user, Doctor):
                return redirect(url_for('auth.dashboard', id=user.id))
            elif isinstance(user, Patient):
                return redirect(url_for('auth.patient_dashboard', id=user.id))

    return render_template('login.html', del_success=del_success)


@auth.route('/logout')
def logout():
    logout_user()
    logout_success = "You have successfully logged out!"
    return render_template('login.html', logout_success=logout_success)


@auth.route('/dashboard/<id>')
@login_required
def dashboard(id):
    user_data = storage._DBStorage__session.query(Doctor).filter_by(id=current_user.id).first()
    if current_user.id != id:
        return render_template('error.html', message='Unauthorized access.')

    return render_template('dashboard.html', user=user_data, user_id=id)


@auth.route('/patient_dashboard/<id>')
@login_required
def patient_dashboard(id):
    user_data = storage._DBStorage__session.query(Patient).filter_by(id=current_user.id).first()
    if current_user.id != id:
        return render_template('error.html', message='Unauthorized access.')

    return render_template('patient_dashboard.html', user=user_data, user_id=id)

@auth.route('/dashboard')
@login_required
def dashboard_redirect():
    # Redirect to the current user's dashboard using their ID
    return redirect(url_for('auth.dashboard', id=current_user.id))


@auth.route('/delete_doctor', methods=['GET'])
def delete_doctor():
    delete_doc_api_url = f"http://127.0.0.1:5000/api/v1/doctor/{current_user.id}"
    response = requests.delete(delete_doc_api_url)
    del_success = "Your account has been deleted successfully!"
    return redirect(url_for('auth.login', del_success=del_success))
