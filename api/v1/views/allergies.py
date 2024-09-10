#!/usr/bin/python3
"""
This module creates view for Allergies objects
"""

from flask import jsonify, request, abort, flash, redirect, url_for, render_template
from api.v1.views import app_views
from models import storage
from models.allergies import Allergies
from models.patient import Patient
from models.doctor import Doctor
from datetime import datetime
from flask_login import login_required, current_user


@app_views.route('/patient/<patient_id>/allergies', methods=['GET'],
                 strict_slashes=False)
def get_patient_allergies(patient_id):
    """Retrieves a Patient's medical allergies based on his/her ID"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()
    if not allergies:
        abort(404, "No allergies found for the specified Patient")
    return jsonify(allergies.to_dict())


@app_views.route('/doctor/patient/<patient_id>/add_allergies',
                 methods=['GET', 'POST'], strict_slashes=False)
@login_required
def add_patient_allergies(patient_id):
    """Creates a Patient's allergies based on his/her ID"""
    if not isinstance(current_user, Doctor):
        abort(403, "You are not authorized to perform this function!")

    # Cchecks if Paatient exist
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    if request.method == 'POST':
        allergen = request.form.get('allergen')
        reaction = request.form.get('reaction')
        severity = request.form.get('severity')
        notes = request.form.get('notes')
        action = request.form.get('action')

        if action == "skip":
            flash('You skipped Patient Allergies', 'success')
            # Redirect to Allergy entry page after creating the patient
            return redirect(url_for('app_views.add_patient_medical_record', patient_id=patient.id))

        if action == "submit":
            # Check for Empty Fields
            if not all([allergen, reaction, severity, notes]):
                flash('Required Fields are Empty!', 'error')
                return render_template('register_allergy.html', patient_id=patient_id, notes=notes,
                                       allergen=allergen, reaction=reaction, severity=severity)

            # Check if Patient has a stored allergy
            existing_allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()
            if existing_allergies:
                flash('Patient already has a registered allergy rocord!', 'error')
                return render_template('register_allergy.html', patient_id=patient_id, notes=notes,
                                       allergen=allergen, reaction=reaction, severity=severity)
            
            # Creates a new allergy record
            new_allergies = Allergies(allergen=allergen, reaction=reaction,
                                    severity=severity, notes=notes)

            try:
                new_allergies.patient_id = patient.id
                storage.new(new_allergies)
                storage.save()
                flash('Patient Allergies added successfully!', 'success')

                # Redirect to Allergy entry page after creating the patient
                return redirect(url_for('app_views.add_patient_medical_record', patient_id=patient.id))
            except Exception as e:
                # abort(500, f"An error occured while saving the allergies: {str(e)}")
                flash(f'Error: {str(e)}', 'error')
                return render_template('register_allergy.html', patient_id=patient_id, notes=notes,
                                       allergen=allergen, reaction=reaction, severity=severity)

    return render_template('register_allergy.html', patient_id=patient_id)


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/update_allergies',
                 methods=['PUT'], strict_slashes=False)
def update_patient_allergies(doctor_id, patient_id):
    """Updates a Patient's allergies based on his/her ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()
    if not allergies:
        abort(404, "Allergies not found for the specified Patient")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(allergies, key, value)

    allergies.updated_at = datetime.utcnow()
    storage.save()
    return jsonify(allergies.to_dict()), 200


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/delete_allergies',
                 methods=['DELETE'], strict_slashes=False)
def delete_patient_allergies(doctor_id, patient_id):
    """Deletes a Patient's allergies based on his/her ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()
    if not allergies:
        abort(404, "Allergies not found for the specified Patient")

    storage.delete(allergies)
    storage.save()
    return jsonify({}), 200
