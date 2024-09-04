#!/usr/bin/python3
"""
Creates a new User and Integrates with Backend Database
"""
from models import storage
from models.patient import Patient
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from auth import auth


@auth.route('/register-patient', methods=['GET', 'POST'])
def register_patient():
    errors = []
    error_empty_fields = ''
    error_pwd_mismatch = ''
    if request.method == "POST":
        first_name = request.form['fname']
        last_name = request.form['lname']
        dob = request.form['dob']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        address = request.form['address']
        zipcode = request.form['zipcode']
        email = request.form['email']
        phone = request.form['phone']
        emg_contact_name = request.form['emg_contact_name']
        emg_contact_phone = request.form['emg_contact_phone']
        password = request.form['password']
        conf_password = request.form['conf_password']

        # Check if all fields are not empty
        if (not first_name or not last_name or not dob or not gender
            or not blood_group or not email or not phone or not emg_contact_name
            or not emg_contact_phone or not password or not conf_password):
            error_empty_fields = 'Required Fields are Empty'
            errors.append(error_empty_fields)

        patient = storage._DBStorage__session.query(Patient).filter_by(email=email).first()

        if patient:
            error_reg_user = 'Patient already exist, use a different email!'
            errors.append(error_reg_user)
            return render_template('register_patient.html', err_reg_user=error_reg_user)

        # Check if passwords match before hashing
        if password != conf_password:
            error_pwd_mismatch = 'Passwords do not match'
            errors.append(error_pwd_mismatch)
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if not errors:
            new_patient = Patient(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone_number=phone,
                            date_of_birth = dob,
                            gender = gender,
                            address = address,
                            zipcode = zipcode,
                            blood_group = blood_group,
                            emergency_contact_name = emg_contact_name,
                            emergency_contact_phone = emg_contact_phone,
                            password=hashed_password)

            try:
                storage.new(new_patient)
                storage.save()
                # register_success = "You have successfully created an account. Please log in!"
                # if not errors:
                #     login_user(new_patient)
                #     return redirect(url_for('healthpixel', id=new_patient.id))
            except Exception as e:
                errors.append(f'Error: {str(e)}')
    return render_template('register_patient.html',
                           error_ef = error_empty_fields,
                           error_pm = error_pwd_mismatch)


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     del_success = request.args.get('del_success')
#     errors = []
#     error_login = ''
#     error_empty_fields = ''
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         remember = 'remember' in request.form
        
#         # Check if all fields are not empty
#         if not email or not password:
#             error_empty_fields = 'All fields are required'
#             errors.append(error_empty_fields)
#             return render_template('login.html', err_ef=error_empty_fields)

#         doctor = storage._DBStorage__session.query(Doctor).filter_by(email=email).first()

#         if not (doctor and check_password_hash(doctor.password, password)):
#             error_login = 'Invalid Login. Check Username or Password!'
#             errors.append(error_login)
#             return render_template('login.html', err_login=error_login)

#         if not errors:
#             login_user(doctor, remember=remember)
#             return redirect(url_for('auth.dashboard', id=doctor.id))

#     return render_template('login.html', del_success=del_success)


# @auth.route('/logout')
# def logout():
#     logout_user()
#     logout_success = "You have successfully logged out!"
#     return render_template('login.html', logout_success=logout_success)


# @auth.route('/dashboard/<id>')
# @login_required
# def dashboard(id):
#     user_data = storage._DBStorage__session.query(Doctor).filter_by(id=current_user.id).first()
#     if current_user.id != id:
#         return render_template('error.html', message='Unauthorized access.')

#     return render_template('dashboard.html', user=user_data, user_id=id)


# @auth.route('/dashboard')
# @login_required
# def dashboard_redirect():
#     # Redirect to the current user's dashboard using their ID
#     return redirect(url_for('auth.dashboard', id=current_user.id))


# @auth.route('/delete_doctor', methods=['GET'])
# def delete_doctor():
#     delete_doc_api_url = f"http://127.0.0.1:5000/api/v1/doctor/{current_user.id}"
#     response = requests.delete(delete_doc_api_url)
#     del_success = "Your account has been deleted successfully!"
#     return redirect(url_for('auth.login', del_success=del_success))
