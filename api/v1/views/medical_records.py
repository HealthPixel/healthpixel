#!/usr/bin/python3
"""
This module creates view for Medical_Record objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.medical_record import Medical_Record
from models.patient import Patient


@app_views.route('/patient/<patient_id>/medical_records', methods=['GET'],
                 strict_slashes=False)
def get_patient_medical_record(patient_id):
    """Retrieves a Patient's medical records based on his/her ID"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient does not exist")

    medical_record = storage._DBStorage__session.query(Medical_Record).filter_by(patient_id=patient_id).first()
    if not medical_record:
        abort(400, "No medical record found for the specified Patient")
    return jsonify(medical_record.to_dict())
