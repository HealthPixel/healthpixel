#!/usr/bin/python3
"""
This module creates view for Patient objects
"""

from flask import jsonify, request, abort, render_template, url_for, flash
from sqlalchemy import text
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor
from models.patient import Patient
from models.access_log import Access_Log
from datetime import datetime
from flask_login import current_user, login_user, login_required
from models.vitals import Vitals
from models.medical_record import Medical_Record
from models.allergies import Allergies


@app_views.route('/doctor/patients', methods=['GET'], strict_slashes=False)
def get_patients():
    """Retrieves a list of all Patients"""
    patients = storage.all(Patient).values()
    return jsonify([patient.to_dict() for patient in patients]), 201


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_patient(doctor_id, patient_id):
    """Retrieves a Patient object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)

    if not doctor:
        abort(400, "Doctor not found")
    if not patient:
        abort(400, "Patient not found")

    # Log the access
    action_taken = "Retrieve a Patient"
    access_log = Access_Log(user_id=doctor_id, patient_id=patient_id, action_taken=action_taken)
    storage.new(access_log)
    storage.save()

    return jsonify(patient.to_dict()), 201


@app_views.route('/doctor/patients/search', methods=['GET'], strict_slashes=False)
def search_patients():
    """Searches for patients by email or ID"""
    query = request.args.get('query', '').strip()
    if not query:
        abort(400, "Query parameter required")

    patients = storage.all(Patient).values()
    matching_patients = [patient for patient in patients if query in patient.email or query == patient.id]

    if not matching_patients:
        return jsonify([]), 200

    return jsonify([patient.to_dict() for patient in matching_patients]), 200


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>', methods=['PUT'], strict_slashes=False)
def update_a_patient(doctor_id, patient_id):
    """Updates a Patient object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)
    if not doctor:
        abort(400, "Doctor not found")
    if not patient:
        abort(404, "Patient not found")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at'] # These keys can't be updated
    for key, value in data.items():
            if key not in ignored_keys:
                if hasattr(patient, key):
                    setattr(patient, key, value)

    try:
        # Log the access
        action_taken = (
            f"{patient.first_name} {patient.last_name}'s record was UPDATED by "
            f"Doctor {doctor.first_name} {doctor.last_name}"
            )
        access_log = Access_Log(user_id=doctor_id, patient_id=patient_id, action_taken=action_taken)
        storage.new(access_log)

        # Save all chnages to database
        patient.updated_at = datetime.utcnow()
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient: {str(e)}")

    return jsonify(patient.to_dict()), 201


@app_views.route('/doctor/patients/<patient_id>/update_patient_records',
                 methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_patient_records(patient_id):
    if not isinstance(current_user, Doctor):
        abort(403, "You are not authorized to perform this function")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient not found")

    if request.method == 'GET':
        vitals = storage.query(Vitals).filter_by(patient_id=patient_id).first()
        medical_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
        allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()

        return render_template('update_patient_records.html',
                               patient=patient,vitals=vitals,
                               medical_record=medical_record,
                               allergies=allergies)

    elif request.method == 'POST':
        data = request.form
        vitals = storage.query(Vitals).filter_by(patient_id=patient_id).first()
        medical_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
        allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()

        if vitals:
            vitals.blood_pressure = data.get('blood_pressure', vitals.blood_pressure)
            vitals.heart_rate = data.get('heart_rate', vitals.heart_rate)
            vitals.save()

        if medical_record:
            medical_record.diagnosis = data.get('diagnosis', medical_record.diagnosis)
            medical_record.treatment = data.get('treatment', medical_record.treatment)
            medical_record.save()

        flash('Patient records updated successfully', 'success')
        return redirect(url_for('app_views.update_patient_records', patient_id=patient_id))


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_patient(doctor_id, patient_id):
    """Deletes a Patient object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)

    if not doctor:
        abort(400, "Doctor not found")
    if not patient:
        abort(404, "Patient not found")

    # Log the access
    action_taken = (
        f"{patient.first_name} {patient.last_name}'s record was DELETED by "
        f"Doctor {doctor.first_name} {doctor.last_name}"
        )
    access_log = Access_Log(user_id=doctor_id, patient_id=patient_id, action_taken=action_taken)
    storage.new(access_log)

    # Disable foreign key checks before deleting
    storage._DBStorage__session.execute(text('SET FOREIGN_KEY_CHECKS = 0'))

    # Deletes the Patient
    storage.delete(patient)
    storage.save()

    # Enables foreign key checks after deleting
    storage._DBStorage__session.execute(text('SET FOREIGN_KEY_CHECKS = 1'))
    return jsonify({}), 200
