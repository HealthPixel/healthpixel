#!/usr/bin/python3
"""
This module creates view for Lab Result objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor
from models.patient import Patient
from models.lab_result import Lab_Results


@app_views.route('/patient/<patient_id>/lab_result', methods=['GET'], strict_slashes=False)
def get_lab_result(patient_id):
    """Retrieves a Patient Lab Result based on the patient_id"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient does not exist")

    lab_result = storage._DBStorage__session.query(Lab_Results).filter_by(patient_id=patient_id).first()
    if not lab_result:
        abort(400, "No Lab Result found for the specified Patient")

    return jsonify(lab_result.to_dict())

@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/lab_result', methods=['POST'], strict_slashes=False)
def create_patient_lab_result(doctor_id, patient_id):
    """Create a Patient Lab Result based on the patient_id"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)

    if not doctor:
        abort(400, "Doctor does not exist!")
    if not patient:
        abort(400, "Patient does not exist!")
    
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    
    required_fields = ['test_name', 'result', 'values']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing {field}")

    existing_record = storage._DBStorage__session.query(Lab_Results).filter_by(patient_id=patient_id).first()
    if existing_record:
        abort(400, "Patient already has a lab result")

    try:
        data['doctor_id'] = doctor_id
        data['patient_id'] = patient_id
        lab_result = Lab_Results(**data)
        storage.new(lab_result)
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient: {str(e)}")

    return (jsonify(lab_result.to_dict())), 201


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/lab_result', methods=['PUT'], strict_slashes=False)
def update_patient_lab_result(doctor_id, patient_id):
    """Updates a Patient  Lab Result based on the medication_id"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(400, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient does not exist")

    lab_result = storage._DBStorage__session.query(Lab_Results).filter_by(patient_id=patient_id).first()
    if not lab_result:
        abort(400, " Lab Result record not found for the specified Patient")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at'] # These keys can't be updated
    for key, value in data.items():
            if key not in ignored_keys:
                if hasattr(lab_result, key):
                    setattr(lab_result, key, value)

    try:
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient Lab Result: {str(e)}")

    return jsonify(lab_result.to_dict()), 201


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/lab_result', methods=['DELETE'], strict_slashes=False)
def delete_patient_lab_result(doctor_id, patient_id):
    """Deletes a Patient Lab Result based on the patient_id"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(400, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient does not exist")

    lab_result = storage._DBStorage__session.query(Lab_Results).filter_by(patient_id=patient_id).first()
    if not lab_result:
        abort(400, "Lab Result not found for the specified Patient")

    storage.delete(lab_result)
    storage.save()
    return jsonify({}), 200
