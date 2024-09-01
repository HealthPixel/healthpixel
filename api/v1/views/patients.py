from flask import Flask, Blueprint, request, jsonify
from models import storage
from models.patient import Patient


patient = Blueprint('patient', __name__)


@patient.route('/create-patient', methods=['GET', 'POST'])
def create_patient():
    # patient_obj = storage._DBStorage__session.query(Patient).all()
    # for patient in patient_obj:
    #     for column in Patient.__table__.columns:
    #         patient_dict[column.name] = getattr(patient, column.name)
    
    if request.method == 'GET':
        patients = storage.all(Patient).values()
        return jsonify([patient.to_dict() for patient in patients]), 201
        # if len(patient_dict) > 0:
        #     return patient_dict
        # else:
        #     return "Nothing Found", 404

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        address = request.form['address']
        zip_code = request.form['zip_code']
        password = request.form['password']
        blood_grp = request.form['blood_grp']
        emergency_cont_name = request.form['emergency_cont_name']
        emergency_cont_phone = request.form['emergency_cont_phone']

        new_patient = Patient(first_name=first_name,
                              last_name=last_name,
                              email=email,
                              phone_number=phone_number,
                              date_of_birth=date_of_birth,
                              gender=gender,
                              address=address,
                              zip_code=zip_code,
                              password=password,
                              blood_grp=blood_grp,
                              emergency_cont_name=emergency_cont_name,
                              emergency_cont_phone=emergency_cont_phone)
        
        try:
            storage.new(new_patient)
            storage.save()
        except Exception as e:
            "Could not Create Patient", 404

        patient_dict = storage.all(Patient)
    
    return jsonify(patient_dict), 201
