#!/usr/bin/python3
"""
This module creates view for Medical_Record objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.medical_record import Medical_Record
from models.patient import Patient
from models.doctor import Doctor
from datetime import datetime


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


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/add_medical_record',
                 methods=['POST'], strict_slashes=False)
def add_patient_medical_record(doctor_id, patient_id):
    """Creates a Patient's medical record based on his/her ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404, "Doctor does not exist")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404, "Patient does not exist")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    required_fields = ['diagnosis', 'prescription', 'treatment', 'visit_date']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing required field {field}")

    existing_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
    if existing_record:
        abort(400, "Patient already has a medical record")

    try:
        data['patient_id'] = patient_id
        data['doctor_id'] = doctor_id
        new_medical_record = Medical_Record(**data)
        storage.new(new_medical_record)
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Medical Record: {str(e)}")

    return jsonify(new_medical_record.to_dict()), 201


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
