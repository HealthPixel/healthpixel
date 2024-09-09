#!/usr/bin/python3
"""
This module creates view for Vitals objects
"""

from flask import jsonify, request, abort, render_template, redirect, url_for, flash
from api.v1.views import app_views
from models import storage
from models.vitals import Vitals
from models.patient import Patient
from models.doctor import Doctor
from datetime import datetime
from flask_login import login_required, current_user


@app_views.route('/patient/<patient_id>/vitals', methods=['GET'],
                 strict_slashes=False)
def get_patient_vitals(patient_id):
    """Retrieves a Patient's medical vitals based on his/her ID"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    vitals = storage.query(Vitals).filter_by(patient_id=patient_id).first()
    if not vitals:
        abort(404, "No vitals found for the specified Patient")
    return jsonify(vitals.to_dict())


@app_views.route('/doctor/patient/<patient_id>/add_vitals',
                 methods=['GET', 'POST'], strict_slashes=False)
@login_required
def add_patient_vitals(patient_id):
    """Creates a Patient's vitals based on his/her ID"""
    if not isinstance(current_user, Doctor):
        abort(403, "You are not authorized to perform this function!")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    if request.method == "POST":
        blood_pressure = request.form.get('blood_pressure')
        heart_rate = request.form.get('heart_rate')
        body_temperature = request.form.get('body_temperature')
        respiratory_rate = request.form.get('respiratory_rate')
        oxygen_saturation = request.form.get('oxygen_saturation')
        weight = request.form.get('weight')
        height = request.form.get('height')

        # Check for Empty Fields
        if not all([blood_pressure, heart_rate, body_temperature, respiratory_rate,
                    oxygen_saturation, weight, height]):
            flash('Required Fields are Empty!', 'error')
            return redirect(url_for('app_views.add_patient_vitals', patient_id=patient.id))

        # Check if Patient has a stored vitals
        existing_vitals = storage.query(Vitals).filter_by(patient_id=patient_id).first()
        if existing_vitals:
            flash('Patient already hass a registered Vital rocord!', 'error')
            return redirect(url_for('app_views.add_patient_vitals', patient_id=patient.id))

        new_vitals = Vitals(blood_pressure=blood_pressure,
                            heart_rate=heart_rate,
                            body_temperature=body_temperature,
                            respiratory_rate=respiratory_rate,
                            oxygen_saturation=oxygen_saturation,
                            weight=weight,
                            height=height)

        try:
            new_vitals.patient_id = patient.id
            storage.new(new_vitals)
            storage.save()
            flash('Patient Vitals added successfully!', 'success')

            # Redirect to Allergy entry page after creating the patient
            return redirect(url_for('app_views.add_patient_allergies', patient_id=patient.id))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('app_views.add_patient_vitals', patient_id=patient.id))

    return render_template('register_vitals.html', patient_id=patient_id)


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/update_vitals',
                 methods=['PUT'], strict_slashes=False)
def update_patient_vitals(doctor_id, patient_id):
    """Updates a Patient's vitals based on his/her ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    vitals = storage.query(Vitals).filter_by(patient_id=patient_id).first()
    if not vitals:
        abort(404, "Vitals not found for the specified Patient")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(vitals, key, value)

    vitals.updated_at = datetime.utcnow()
    storage.save()
    return jsonify(vitals.to_dict()), 200


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/delete_vitals',
                 methods=['DELETE'], strict_slashes=False)
def delete_patient_vitals(doctor_id, patient_id):
    """Deletes a Patient's vitals based on his/her ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    vitals = storage.query(Vitals).filter_by(patient_id=patient_id).first()
    if not vitals:
        abort(404, "Vitals not found for the specified Patient")

    storage.delete(vitals)
    storage.save()
    return jsonify({}), 200
