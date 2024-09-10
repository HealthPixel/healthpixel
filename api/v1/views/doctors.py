#!/usr/bin/python3
"""
This module creates view for Doctor objects
"""

from flask import jsonify, request, abort, render_template, flash, redirect, url_for
from sqlalchemy import text
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor
from models.patient import Patient
from models.access_log import Access_Log
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from datetime import datetime


@app_views.route('/doctors', methods=['GET'], strict_slashes=False)
def get_doctors():
    """Retrieves a list of all Doctors"""
    doctors = storage.all(Doctor).values()
    return jsonify([doctor.to_dict() for doctor in doctors])


@app_views.route('/doctor/<doctor_id>', methods=['GET'], strict_slashes=False)
def get_a_doctor(doctor_id):
    """Retrieves a Doctor object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(400, "Doctor does not exist!")
    return jsonify(doctor.to_dict())


@app_views.route('/doctor/<doctor_id>/update_doctor', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_a_doctor(doctor_id):
    """Updates a Doctor object based on its ID"""
    # Ensure the user is a Doctor
    if not isinstance(current_user, Doctor):
        abort(403, "You are not authorized to perform this function!")
    
    # Checks if Doctor exists
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        flash('Doctor does not exist!', 'error')
        abort(400, "Doctor does not exist!")

    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        specialization = request.form['specialization']
        password = request.form['password']
        conf_password = request.form['conf_password']

        # Check if passwords match before hashing
        if password and conf_password:
            if password != conf_password:
                flash('Passwords do not match', 'error')
                return render_template('update_doctor.html',
                            first_name=doctor.first_name, last_name=doctor.last_name,
                            email=doctor.email, phone_number=doctor.phone_number,
                            specialization=doctor.specialization)
            else:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            doctor.first_name = first_name
            doctor.last_name = last_name
            doctor.email = email
            doctor.phone_number = phone_number
            doctor.specialization = specialization

            # Time and Date of Update
            doctor.updated_at = datetime.utcnow()

            # Only update the password if it's provided
            if password and conf_password:
                doctor.password = hashed_password

            storage.new(doctor)
            storage.save()
            flash('Doctors Profile Updated Successfully!', 'success')
            return redirect(url_for('auth.dashboard_doctor', id=doctor.id))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template('update_doctor.html',
                           first_name=doctor.first_name, last_name=doctor.last_name,
                           email=doctor.email, phone_number=doctor.phone_number,
                           specialization=doctor.specialization)


@app_views.route('/doctor/<doctor_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_doctor(doctor_id):
    """Deletes a Doctor object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404)

    # Disable foreign key checks before deleting
    storage._DBStorage__session.execute(text('SET FOREIGN_KEY_CHECKS = 0'))

    storage.delete(doctor)
    storage.save()

    # Enables foreign key checks after deleting
    storage._DBStorage__session.execute(text('SET FOREIGN_KEY_CHECKS = 1'))
    return jsonify({}), 200


@app_views.route('/doctor/register-patient', methods=['GET', 'POST'],
                 strict_slashes=False)
@login_required
def register_patient():
    """Creates a Patient object"""
    # Ensure the user is a Doctor
    if not isinstance(current_user, Doctor):
        abort(403, "You are not authorized to perform this function!")

    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        address = request.form.get('address')
        zipcode = request.form.get('zipcode')
        blood_group = request.form.get('blood_group')
        emg_contact_name = request.form.get('emg_contact_name')
        emg_contact_phone = request.form.get('emg_contact_phone')
        password = request.form.get('password')
        conf_password = request.form.get('conf_password')

        # Check if all fields are not empty
        if (not first_name or not last_name or not date_of_birth or not gender
            or not blood_group or not email or not phone_number or not emg_contact_name
            or not emg_contact_phone):
            flash('Required Fields are Empty!', 'error')
            return render_template('register_patient.html', first_name=first_name, last_name=last_name,
                                   date_of_birth=date_of_birth, gender=gender, blood_group=blood_group,
                                   email=email, phone_number=phone_number, address=address,
                                   zipcode=zipcode, emg_contact_name=emg_contact_name,
                                   emg_contact_phone=emg_contact_phone)

        # Check if Patient exists using email as a unique identifier
        patient = storage.query(Patient).filter_by(email=email).first()
        if patient:
            flash('Patient already exists, use a different email!', 'error')
            return render_template('register_patient.html', first_name=first_name, last_name=last_name,
                                   date_of_birth=date_of_birth, gender=gender, blood_group=blood_group,
                                   phone_number=phone_number, address=address, zipcode=zipcode,
                                   emg_contact_name=emg_contact_name, emg_contact_phone=emg_contact_phone)

        # Check if passwords match before hashing
        if password != conf_password:
            flash('Passwords do not match', 'error')
            return render_template('register_patient.html', first_name=first_name, last_name=last_name,
                                   date_of_birth=date_of_birth, gender=gender, blood_group=blood_group,
                                   email=email, phone_number=phone_number, address=address,
                                   zipcode=zipcode, emg_contact_name=emg_contact_name,
                                   emg_contact_phone=emg_contact_phone)
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Creates a new Patient 
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
            flash("You have successfully created a Patient account!", 'success')

            # Redirect to Vitals entry page after creating the patient
            return redirect(url_for('app_views.add_patient_vitals', patient_id=new_patient.id))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return render_template('register_patient.html', first_name=first_name, last_name=last_name,
                                   date_of_birth=date_of_birth, gender=gender, blood_group=blood_group,
                                   email=email, phone_number=phone_number,
                                   emg_contact_name=emg_contact_name, emg_contact_phone=emg_contact_phone)

    return render_template('register_patient.html')
