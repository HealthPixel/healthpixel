#!/usr/bin/python3
"""
This module creates view for Lab Result objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment


@app_views.route('/patient/appointment/<appointment_id>', methods=['GET'], strict_slashes=False)
def get_appointment(appointment_id):
    """Retrieves a Patient Appointment based on the patient_id"""
    appointment = storage.get(Appointment, appointment_id)
    if not appointment:
        abort(400, "No Appointment found!")

    return jsonify(appointment.to_dict()), 200


@app_views.route('/patient/<patient_id>/appointments', methods=['GET'], strict_slashes=False)
def get_appointments(patient_id):
    """Retrieves a list of Patient Appointments based on the patient_id"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient does not exist")

    appointments = storage._DBStorage__session.query(Appointment).filter_by(patient_id=patient_id).all()
    if not appointments:
        abort(400, "No Appointment found for the specified Patient")

    return jsonify([appointment.to_dict() for appointment in appointments]), 200


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>/appointment/<appointment_id>',
                 methods=['POST'], strict_slashes=False)
def create_appointment(doctor_id, patient_id):
    """Create a Patient Appointment based on the patient_id"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)

    if not doctor:
        abort(400, "Doctor does not exist!")
    if not patient:
        abort(400, "Patient does not exist!")
    
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    
    required_fields = ['appointment_date', 'status']
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing {field}")

    # existing_record = storage._DBStorage__session.query(Appointment).filter_by(patient_id=patient_id).first()
    # if existing_record:
    #     abort(400, "Patient already has an Appointment")

    try:
        data['doctor_id'] = doctor_id
        data['patient_id'] = patient_id
        appointment = Appointment(**data)
        storage.new(appointment)
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient: {str(e)}")

    return (jsonify(appointment.to_dict())), 201


@app_views.route('/patient/appointment/<appointment_id>', methods=['PUT'], strict_slashes=False)
def update_appointment(appointment_id):
    """Updates a Patient  Appointment based on the appointment_id"""
    appointment = storage.get(Appointment, appointment_id)
    if not appointment:
        abort(400, "No Appointment found for the specified Patient")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at'] # These keys can't be updated
    for key, value in data.items():
            if key not in ignored_keys:
                if hasattr(appointment, key):
                    setattr(appointment, key, value)

    try:
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient Lab Result: {str(e)}")

    return jsonify(appointment.to_dict()), 201


@app_views.route('/patient/appointment/<appointment_id>', methods=['DELETE'], strict_slashes=False)
def delete_appointment(appointment_id):
    """Deletes a Patient Appointment based on the appointment_id"""
    appointment = storage.get(Appointment, appointment_id)
    if not appointment:
        abort(400, "No Appointment found for the specified Patient")

    storage.delete(appointment)
    storage.save()
    return jsonify({}), 200
