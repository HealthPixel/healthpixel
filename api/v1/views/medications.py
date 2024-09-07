#!/usr/bin/python3
"""
This module creates view for Medication objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor
from models.patient import Patient
from models.medication import Medication
from datetime import datetime


@app_views.route('/patient/<patient_id>/medication', methods=['GET'], strict_slashes=False)
def get_patient_medication(patient_id):
    """Retrieves a Patient Medication based on the patient_id"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient does not exist")

    medication = storage.query(Medication).filter_by(patient_id=patient_id).first()
    if not medication:
        abort(400, "No medication found for the specified Patient")

    return jsonify(medication.to_dict())


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/medication', methods=['POST'], strict_slashes=False)
def create_patient_medication(doctor_id, patient_id):
    """Create a Patient Medication based on the patient_id"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)

    if not doctor:
        abort(400, "Doctor does not exist!")
    if not patient:
        abort(400, "Patient does not exist!")
    
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    
    required_fields = ['medicine_name', 'dosage', 'frequency', 'duration']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing {field}")

    existing_record = storage.query(Medication).filter_by(patient_id=patient_id).first()
    if existing_record:
        abort(400, "Patient already has a medication")

    try:
        data['doctor_id'] = doctor_id
        data['patient_id'] = patient_id
        medication = Medication(**data)
        storage.new(medication)
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient: {str(e)}")

    return (jsonify(medication.to_dict())), 201


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/medication', methods=['PUT'], strict_slashes=False)
def update_patient_medication(doctor_id, patient_id):
    """Updates a Patient Medication based on patient_id"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(400, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient does not exist")

    medication = storage.query(Medication).filter_by(patient_id=patient_id).first()
    if not medication:
        abort(400, " Medication record not found for the specified Patient")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at'] # These keys can't be updated
    for key, value in data.items():
            if key not in ignored_keys:
                if hasattr(medication, key):
                    setattr(medication, key, value)

    try:
        medication.updated_at = datetime.utcnow()
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient Medication: {str(e)}")

    return jsonify(medication.to_dict()), 201


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/medication', methods=['DELETE'], strict_slashes=False)
def delete_patient_medication(doctor_id, patient_id):
    """Deletes a Patient Mediaction based on the patient_id"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(400, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient does not exist")

    medication = storage.query(Medication).filter_by(patient_id=patient_id).first()
    if not medication:
        abort(400, "Medication not found for the specified Patient")

    storage.delete(medication)
    storage.save()
    return jsonify({}), 200
