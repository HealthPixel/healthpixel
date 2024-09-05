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
@login_required
def register_patient():
    errors = []
    error_empty_fields = ''
    error_pwd_mismatch = ''
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        address = request.form.get('address')
        zipcode = request.form.get('zipcode')
        password = request.form.get('password')
        blood_group = request.form.get('blood_group')
        emg_contact_name = request.form.get('emg_contact_name')
        emg_contact_phone = request.form.get('emg_contact_phone')
        password = request.form.get('password')
        conf_password = request.form.get('conf_password')

        # Check if all fields are not empty
        if (not first_name or not last_name or not date_of_birth or not gender
            or not blood_group or not email or not phone_number or not emg_contact_name
            or not emg_contact_phone):
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
                            phone_number=phone_number,
                            date_of_birth = date_of_birth,
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
                register_success = "You have successfully created a Patient account!"
                if not errors:
                    flash(register_success)
                    return redirect(url_for('auth.dashboard_doctor', id=current_user.id))
            except Exception as e:
                errors.append(f'Error: {str(e)}')
    return render_template('register_patient.html',
                           error_ef = error_empty_fields,
                           error_pm = error_pwd_mismatch)


@auth.route('/logout_patient')
def logout_patient():
    logout_user()
    logout_success = "You have successfully logged out!"
    return render_template('login.html', logout_success=logout_success)


@auth.route('/patient_dashboard/<id>')
@login_required
def dashboard_patient(id):
    user_data = storage._DBStorage__session.query(Patient).filter_by(id=current_user.id).first()
    if current_user.id != id:
        return render_template('error.html', message='Unauthorized access.')

    return render_template('patient_dashboard.html', user=user_data, user_id=id)


# @auth.route('/dashboard')
# @login_required
# def dashboard_redirect_patient():
#     # Redirect to the current user's dashboard using their ID
#     return redirect(url_for('auth.dashboard', id=current_user.id))


# @auth.route('/delete_doctor', methods=['GET'])
# def delete_doctor():
#     delete_doc_api_url = f"http://127.0.0.1:5000/api/v1/doctor/{current_user.id}"
#     response = requests.delete(delete_doc_api_url)
#     del_success = "Your account has been deleted successfully!"
#     return redirect(url_for('auth.login', del_success=del_success))
