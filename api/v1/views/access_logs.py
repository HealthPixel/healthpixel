#!/usr/bin/python3
"""
This module creates views for Access_Log objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.access_log import Access_Log


@app_views.route('/access_logs', methods=['GET'], strict_slashes=False)
def get_access_logs():
    """Retrieves a list of all Access_Logs"""
    logs = storage.all(Access_Log).values()
    return jsonify([log.to_dict() for log in logs])


@app_views.route('/access_logs/patient/<patient_id>', methods=['GET'],
                 strict_slashes=False)
def get_access_logs_by_patient(patient_id):
    """Retrieves access logs for a specific patient"""
    logs = storage.query(Access_Log).filter_by(patient_id=patient_id).all()
    if not logs:
        abort(400, "No access logs found for the specified Patient")
    return jsonify([log.to_dict() for log in logs])


@app_views.route('/access_logs/doctor/<doctor_id>', methods=['GET'],
                 strict_slashes=False)
def get_access_logs_by_doctor(doctor_id):
    """Retrieves access logs for a specific doctor"""
    logs = storage.query(Access_Log).filter_by(user_id=doctor_id).all()
    if not logs:
        abort(400, "No access logs found for the specified Doctor")
    return jsonify([log.to_dict() for log in logs])
