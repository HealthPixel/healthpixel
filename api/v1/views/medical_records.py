#!/usr/bin/python3
"""
This module creates view for Medical_Record objects
"""

from flask import jsonify, request, abort, flash, redirect, url_for, render_template
from api.v1.views import app_views
from models import storage
from models.medical_record import Medical_Record
from models.patient import Patient
from models.doctor import Doctor
from datetime import datetime
from flask_login import login_required, current_user


@app_views.route('/patient/<patient_id>/medical_record', methods=['GET'],
                 strict_slashes=False)
def get_patient_medical_record(patient_id):
    """Retrieves a Patient's medical record based on his/her ID"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    medical_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
    if not medical_record:
        abort(404, "No medical record found for the specified Patient")
    return jsonify(medical_record.to_dict())


@app_views.route('/doctor/patient/<patient_id>/add_medical_record',
                 methods=['GET', 'POST'], strict_slashes=False)
@login_required
def add_patient_medical_record(patient_id):
    """Creates a Patient's medical record based on his/her ID"""
    if not isinstance(current_user, Doctor):
        abort(403, "You are not authorized to perform this function!")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')
        treatment = request.form.get('treatment')
        prescription = request.form.get('prescription')
        visit_date = request.form.get('visit_date')
        notes = request.form.get('notes')

        # Check for Empty Fields
        if not all([diagnosis, treatment, prescription, visit_date, notes]):
            flash('Required Fields are Empty!', 'error')
            return redirect(url_for('app_views.add_patient_medical_record', patient_id=patient.id))

        # Check if Patient has a stored allergy
        existing_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
        if existing_record:
            flash('Patient already has a registered allergy rocord!', 'error')
            return redirect(url_for('app_views.add_patient_medical_record', patient_id=patient.id))
        
        new_medical_record = Medical_Record(diagnosis=diagnosis, treatment=treatment,
                                            prescription=prescription, visit_date=visit_date,
                                            notes=notes)

        try:
            new_medical_record.patient_id = patient.id
            new_medical_record.doctor_id = current_user.id
            storage.new(new_medical_record)
            storage.save()
            flash('Patient Medical Records added successfully!', 'success')

            # Redirect to Allergy entry page after creating the patient
            return redirect(url_for('auth.dashboard_doctor'))
        except Exception as e:
            # abort(500, f"An error occured while saving the Medical Record: {str(e)}")
            flash(f'Error: {str(e)}')
            return redirect(url_for('app_views.add_patient_medical_record', patient_id=patient.id))

    return render_template('register_medical_record.html', patient_id=patient_id)


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/update_medical_record',
                 methods=['PUT'], strict_slashes=False)
def update_patient_medical_record(doctor_id, patient_id):
    """Updates a Patient's medical record based on his/her ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    medical_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
    if not medical_record:
        abort(404, "Medical record not found for the specified Patient")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(medical_record, key, value)

    medical_record.updated_at = datetime.utcnow()
    storage.save()
    return jsonify(medical_record.to_dict()), 200


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/delete_medical_record',
                 methods=['DELETE'], strict_slashes=False)
def delete_patient_medical_record(doctor_id, patient_id):
    """Deletes a Patient's medical record based on his/her ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    medical_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
    if not medical_record:
        abort(404, "Medical record not found for the specified Patient")

    storage.delete(medical_record)
    storage.save()
    return jsonify({}), 200
