#!/usr/bin/python3
"""
This module creates view for Doctor objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor
from models.patient import Patient


@app_views.route('/doctors', methods=['GET'], strict_slashes=False)
def get_doctors():
    """Retrieves a list of all Doctors"""
    doctors = storage.all(Doctor).values()
    return jsonify([doctor.to_dict() for doctor in doctors])


@app_views.route('/doctors/<doctor_id>', methods=['GET'], strict_slashes=False)
def get_a_doctor(doctor_id):
    """Retrieves a Doctor object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404)
    return jsonify(doctor.to_dict())


@app_views.route('/doctors/<doctor_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_doctor(doctor_id):
    """Deletes a Doctor object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404)
    storage.delete(doctor)
    storage.save()
    return jsonify({}), 200


@app_views.route('/doctors/add_patient', methods=['POST'], strict_slashes=False)
def create_a_patient():
    """Creates a Patient object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    new_patient = Patient(**data)
    storage.new(new_patient)
    storage.save()
    return jsonify(new_patient.to_dict()), 201


@app_views.route('/doctors/<doctor_id>', methods=['PUT'], strict_slashes=False)
def update_a_doctor(doctor_id):
    """Updates a Doctor object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(doctor, key, value)
    storage.save()
    return jsonify(doctor.to_dict()), 200
