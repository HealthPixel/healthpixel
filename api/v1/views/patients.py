from flask import Flask, request, jsonify, abort
from models import storage
from models.patient import Patient
from api.v1.views import app_views


@app_views.route('/patients', methods=['GET'])
def patients():
    patients = storage.all(Patient).values()
    if not patients:
        return {"Result": "Patients not Found"}, 404
    
    return jsonify([patient.to_dict() for patient in patients]), 201


@app_views.route('/patient/<id>', methods=['GET', 'POST'])
def patient(id):
    if request.method == 'GET':
        patient = storage.get(Patient, id)
        if not patient:
            return {"Result": "Patient not Found"}, 404
        
        return jsonify(patient.to_dict()), 201
