#!/usr/bin/python3
"""
This module creates view for Patient objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor
from models.patient import Patient
from models.access_log import Access_Log


@app_views.route('/doctors/patients', methods=['GET'], strict_slashes=False)
def get_patients():
    """Retrieves a list of all Patients"""
    patients = storage.all(Patient).values()
    return jsonify([patient.to_dict() for patient in patients]), 201


@app_views.route('/doctors/<doctor_id>/patients/<patient_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_patient(doctor_id, patient_id):
    """Retrieves a Patient object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)

    if not doctor:
        abort(404, "Doctor not found")
    if not patient:
        abort(404, "Patient not found")

    # Log the access
    access_log = Access_Log(user_id=doctor_id, patient_id=patient_id)
    storage.new(access_log)
    storage.save()

    return jsonify(patient.to_dict()), 201
