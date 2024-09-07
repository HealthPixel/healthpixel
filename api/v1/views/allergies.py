#!/usr/bin/python3
"""
This module creates view for Allergies objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.allergies import Allergies
from models.patient import Patient
from models.doctor import Doctor
from datetime import datetime


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


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/add_allergies',
                 methods=['POST'], strict_slashes=False)
def add_patient_allergies(doctor_id, patient_id):
    """Creates a Patient's allergies based on his/her ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    required_fields = ['blood_pressure', 'heart_rate', 'body_temperature',
                       'respiratory_rate', 'oxygen_saturation', 'weight',
                       'height']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing required field {field}")

    existing_allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()
    if existing_allergies:
        abort(400, "Patient already has a allergies")

    try:
        data['patient_id'] = patient_id
        new_allergies = Allergies(**data)
        storage.new(new_allergies)
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the allergies: {str(e)}")

    return jsonify(new_allergies.to_dict()), 201


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
