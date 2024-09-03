#!/usr/bin/python3
"""
This module creates view for Vitals objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.vitals import Vitals
from models.patient import Patient
from models.doctor import Doctor


@app_views.route('/patient/<patient_id>/vitals', methods=['GET'],
                 strict_slashes=False)
def get_patient_vitals(patient_id):
    """Retrieves a Patient's medical vitals based on his/her ID"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    vitals = storage._DBStorage__session.query(Vitals).filter_by(patient_id=patient_id).first()
    if not vitals:
        abort(404, "No vitals found for the specified Patient")
    return jsonify(vitals.to_dict())


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/add_vitals',
                 methods=['POST'], strict_slashes=False)
def add_patient_vitals(doctor_id, patient_id):
    """Creates a Patient's vitals based on his/her ID"""
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

    existing_vitals = storage._DBStorage__session.query(Vitals).filter_by(patient_id=patient_id).first()
    if existing_vitals:
        abort(400, "Patient already has a vitals")

    try:
        data['patient_id'] = patient_id
        new_vitals = Vitals(**data)
        storage.new(new_vitals)
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the vitals: {str(e)}")

    return jsonify(new_vitals.to_dict()), 201


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

    vitals = storage._DBStorage__session.query(Vitals).filter_by(patient_id=patient_id).first()
    if not vitals:
        abort(404, "Vitals not found for the specified Patient")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(vitals, key, value)
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

    vitals = storage._DBStorage__session.query(Vitals).filter_by(patient_id=patient_id).first()
    if not vitals:
        abort(404, "Vitals not found for the specified Patient")

    storage.delete(vitals)
    storage.save()
    return jsonify({}), 200
