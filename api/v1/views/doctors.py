#!/usr/bin/python3
"""
This module creates view for Doctor objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor
from models.patient import Patient
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash


@app_views.route('/doctors', methods=['GET'], strict_slashes=False)
def get_doctors():
    """Retrieves a list of all Doctors"""
    doctors = storage.all(Doctor).values()
    return jsonify([doctor.to_dict() for doctor in doctors])


@app_views.route('/doctor/<doctor_id>', methods=['GET'], strict_slashes=False)
def get_a_doctor(doctor_id):
    """Retrieves a Doctor object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404)
    return jsonify(doctor.to_dict())


@app_views.route('/doctor/<doctor_id>', methods=['PUT'], strict_slashes=False)
def update_a_doctor(doctor_id):
    """Updates a Doctor object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404, "Doctor does not exist!")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(doctor, key, value)
    storage.save()
    return jsonify(doctor.to_dict()), 200


@app_views.route('/doctor/<doctor_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_doctor(doctor_id):
    """Deletes a Doctor object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404)
    storage.delete(doctor)
    storage.save()
    return jsonify({}), 200


@app_views.route('/doctor/register-patient', methods=['POST'], strict_slashes=False)
def create_a_patient():
    """Creates a Patient object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    required_fields = ['first_name', 'last_name', 'date_of_birth', 'gender',
                       'blood_group', 'phone_number', 'email',
                       'emergency_contact_name', 'emergency_contact_phone',
                       'password']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing {field}")

    try:
        data['password'] = generate_password_hash(data['password'],
                                                  method='pbkdf2:sha256')

        new_patient = Patient(**data)
        storage.new(new_patient)
        storage.save()
    except IntegrityError:
        abort(400, "A patient with the same email already exists!")
    except Exception as e:
        abort(500, f"An error occured while saving the Patient: {str(e)}")

    return jsonify(new_patient.to_dict()), 201
