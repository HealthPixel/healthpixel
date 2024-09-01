#!/usr/bin/python3
"""
This module creates view for Doctor objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor


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
