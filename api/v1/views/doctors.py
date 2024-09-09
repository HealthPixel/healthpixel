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


@app_views.route('/doctor/<doctor_id>', methods=['PUT'], strict_slashes=False)
def update_a_doctor(doctor_id):
    """Updates a Doctor object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(400, "Doctor does not exist!")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at'] # These keys can't be updated
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(doctor, key, value)

    doctor.updated_at = datetime.utcnow()
    storage.save()
    return jsonify(doctor.to_dict()), 200


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
            flash('Required Fields are Empty!')
            return redirect(url_for('app_views.register_patient'))

        patient = storage.query(Patient).filter_by(email=email).first()

        if patient:
            flash('Patient already exist, use a different email!')
            return redirect(url_for('app_views.register_patient'))

        # Check if passwords match before hashing
        if password != conf_password:
            flash('Passwords do not match')
            return redirect(url_for('app_views.register_patient'))
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

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
            flash(f'Error: {str(e)}')
            return redirect(url_for('app_views.register_patient'))

    return render_template('register_patient.html')
