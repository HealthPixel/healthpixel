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


@app_views.route('/medication/patient/<patient_id>', methods=['GET'], strict_slashes=False)
def get_patient_medication(patient_id):
    """Retrieves a Patient Medication based on the patient_id"""
    med = storage.get(Medication, patient_id)
    return (jsonify(med))


@app_views.route('/medication/patient/<patient_id>', methods=['POST'], strict_slashes=False)
def create_patient_medication():
    """Create a Patient Medication based on the patient_id"""
    pass


@app_views.route('/medication/patient/<patient_id>', methods=['PUT'], strict_slashes=False)
def update_patient_medication():
    """Updates a Patient Medication based on the patient_id"""
    pass


@app_views.route('/medication/patient/<patient_id>', methods=['DELETE'], strict_slashes=False)
def delete_patient_medication(patient_id):
    """Deletes a Patient Mediaction based on the patient_id"""
    patient_meds = storage.get(Medication, patient_id)
    storage.delete(patient_meds)
    storage.save()
    meds = storage.all(Medication).Values()
    return (jsonify([med.to_dict() for med in meds]))