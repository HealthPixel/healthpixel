from flask import Flask, request, jsonify, abort
from models import storage
from models.patient import Patient
from api.v1.views import app_views


@app_views.route('/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'GET':
        patients = storage.all(Patient).values()
        if not patients:
            return {"Result": "Patients not Found"}, 404
        
        return jsonify([patient.to_dict() for patient in patients]), 201

    # if request.method == 'POST':
    #     first_name = request.form['first_name']
    #     last_name = request.form['last_name']
    #     email = request.form['email']
    #     phone_number = request.form['phone_number']
    #     date_of_birth = request.form['date_of_birth']
    #     gender = request.form['gender']
    #     address = request.form['address']
    #     zipcode = request.form['zipcode']
    #     password = request.form['password']
    #     blood_group = request.form['blood_group']
    #     emergency_contact_name = request.form['emergency_contact_name']
    #     emergency_contact_phone = request.form['emergency_contact_phone']

    #     new_patient = Patient(first_name=first_name, last_name=last_name,
    #                           email=email, phone_number=phone_number,
    #                           date_of_birth=date_of_birth, gender=gender,
    #                           address=address, zipcode=zipcode,
    #                           password=password, blood_group=blood_group,
    #                           emergency_contact_name=emergency_contact_name,
    #                           emergency_contact_phone=emergency_contact_phone)
        
    #     try:
    #         storage.new(new_patient)
    #         storage.save()
    #     except Exception as e:
    #         "Could not Create Patient", 404

    #     patients = storage.all(Patient).values()
    #     return jsonify([patient.to_dict() for patient in patients]), 201


@app_views.route('/patient/<id>', methods=['GET', 'POST'])
def patient(id):
    patient = storage.get(Patient, id)
    if not patient:
        return {"Result": "Patient not Found"}, 404
    return jsonify(patient.to_dict())