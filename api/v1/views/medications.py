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


@app_views.route('/patient/<patient_id>/medications', methods=['GET'], strict_slashes=False)
def get_patient_medications(patient_id):
    """Retrieves a Patient Medication based on the patient_id"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        # abort(400, "Patient does not exist")
        return jsonify({"Response": "Patient does not exist"}), 400

    # medication = storage._DBStorage__session.query(Medication).filter_by(patient_id=patient_id).first()
    all_meds = storage.all(Medication).values()
    medication = [meds.to_dict() for meds in all_meds if meds.patient_id == patient_id]

    if not medication:
        # abort(400, "No Medication for the specified patient!")
        return jsonify({"Response": "No Medication for the specified patient"}), 400

    return (jsonify(medication)), 201


@app_views.route('/patient/medication/<medication_id>', methods=['GET'], strict_slashes=False)
def get_a_patient_medication(medication_id):
    """Retrieves a Patient Medication based on the patient_id"""
    medication = storage.get(Medication, medication_id)
    if not medication:
        return jsonify({"Response": "Medication does not exist"}), 400

    return (jsonify(medication.to_dict())), 201


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/medication', methods=['POST'], strict_slashes=False)
def create_patient_medication(doctor_id, patient_id):
    """Create a Patient Medication based on the patient_id"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)

    if not doctor:
        return jsonify({"Response": "Doctor does not exist!"})
    if not patient:
        return jsonify({"Response": "Patient does not exist!"})
    
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    
    required_fields = ['medicine_name', 'dosage', 'frequency', 'duration']
    for field in required_fields:
        if field not in data:
            return jsonify({"Response": f"Missing {field}"})
    try:
        data['doctor_id'] = doctor_id
        data['patient_id'] = patient_id
        medication = Medication(**data)
        storage.new(medication)
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient: {str(e)}")
    return (jsonify(medication.to_dict())), 201


@app_views.route('/patient/medication/<medication_id>', methods=['PUT'], strict_slashes=False)
def update_patient_medication(medication_id):
    """Updates a Patient Medication based on the medication_id"""
    medication = storage.get(Medication, medication_id)
    if not medication:
        abort(404, "Medication not found")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at'] # These keys can't be updated
    for key, value in data.items():
            if key not in ignored_keys:
                if hasattr(medication, key):
                    setattr(medication, key, value)

    try:
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient Medication: {str(e)}")

    return jsonify(medication.to_dict()), 201


@app_views.route('/patient/medication/<medication_id>', methods=['DELETE'], strict_slashes=False)
def delete_patient_medication(medication_id):
    """Deletes a Patient Mediaction based on the patient_id"""
    medication = storage.get(Medication, medication_id)
    storage.delete(medication)
    storage.save()
    return jsonify({}), 200
