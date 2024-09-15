#!/usr/bin/python3
"""
This module creates view for Patient objects
"""

from flask import jsonify, request, abort, render_template, url_for, flash, redirect
from sqlalchemy import text
from api.v1.views import app_views
from models import storage
from models.doctor import Doctor
from models.patient import Patient
from models.access_log import Access_Log
from datetime import datetime
from flask_login import current_user, login_required
from models.vitals import Vitals
from models.medical_record import Medical_Record
from models.allergies import Allergies
from models.appointment import Appointment
from models.lab_result import Lab_Results
from models.medication import Medication


@app_views.route('/doctor/patients', methods=['GET'], strict_slashes=False)
def get_patients():
    """Retrieves a list of all Patients"""
    patients = storage.all(Patient).values()
    return jsonify([patient.to_dict() for patient in patients]), 201


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_patient(doctor_id, patient_id):
    """Retrieves a Patient object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)

    if not doctor:
        abort(400, "Doctor not found")
    if not patient:
        abort(400, "Patient not found")

    # Log the access
    action_taken = "Retrieve a Patient"
    access_log = Access_Log(user_id=doctor_id, patient_id=patient_id, action_taken=action_taken)
    storage.new(access_log)
    storage.save()

    return jsonify(patient.to_dict()), 201


@app_views.route('/doctor/patients/search', methods=['GET'], strict_slashes=False)
def search_patients():
    """Searches for patients by email or ID"""
    query = request.args.get('query', '').strip()
    if not query:
        abort(400, "Query parameter required")

    patients = storage.all(Patient).values()
    matching_patients = [patient for patient in patients if query in patient.email or query == patient.id]

    if not matching_patients:
        return jsonify([]), 200

    return jsonify([patient.to_dict() for patient in matching_patients]), 200


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>', methods=['PUT'], strict_slashes=False)
def update_a_patient(doctor_id, patient_id):
    """Updates a Patient object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)
    if not doctor:
        abort(400, "Doctor not found")
    if not patient:
        abort(404, "Patient not found")

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'created_at'] # These keys can't be updated
    for key, value in data.items():
            if key not in ignored_keys:
                if hasattr(patient, key):
                    setattr(patient, key, value)

    try:
        # Log the access
        action_taken = (
            f"{patient.first_name} {patient.last_name}'s record was UPDATED by "
            f"Doctor {doctor.first_name} {doctor.last_name}"
            )
        access_log = Access_Log(user_id=doctor_id, patient_id=patient_id, action_taken=action_taken)
        storage.new(access_log)

        # Save all chnages to database
        patient.updated_at = datetime.utcnow()
        storage.save()
    except Exception as e:
        abort(500, f"An error occured while saving the Patient: {str(e)}")

    return jsonify(patient.to_dict()), 201


@app_views.route('/doctor/patients/<patient_id>/update_patient_records',
                 methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_patient_records(patient_id):
    """Updates a patients records based on their ID"""
    if not isinstance(current_user, Doctor):
        abort(403, "You are not authorized to perform this function")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient not found")

    if request.method == 'GET':
        vitals = storage.query(Vitals).filter_by(patient_id=patient_id).first()
        medical_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
        allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()
        appointment = storage.query(Appointment).filter_by(patient_id=patient_id).first()
        lab_result = storage.query(Lab_Results).filter_by(patient_id=patient_id).first()
        medication = storage.query(Medication).filter_by(patient_id=patient_id).first()

        return render_template('update_patient_records.html',
                               patient=patient, vitals=vitals,
                               medical_record=medical_record, allergies=allergies,
                               appointment=appointment,lab_result=lab_result,
                               medication=medication)

    elif request.method == 'POST':
        data = request.form
        vitals = storage.query(Vitals).filter_by(patient_id=patient_id).first()
        medical_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
        allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()
        appointment = storage.query(Appointment).filter_by(patient_id=patient_id).first()
        lab_result = storage.query(Lab_Results).filter_by(patient_id=patient_id).first()
        medication = storage.query(Medication).filter_by(patient_id=patient_id).first()

        try:
            # Vitals Update
            if vitals:
                vitals.blood_pressure = data.get('blood_pressure', vitals.blood_pressure)
                vitals.heart_rate = data.get('heart_rate', vitals.heart_rate)
                vitals.body_temperature = data.get('body_temperature', vitals.body_temperature)
                vitals.respiratory_rate = data.get('respiratory_rate', vitals.respiratory_rate)
                vitals.oxygen_saturation = data.get('oxygen_saturation', vitals.oxygen_saturation)
                vitals.weight = data.get('weight', vitals.weight)
                vitals.height = data.get('height', vitals.height)
                vitals.updated_at = datetime.utcnow()
            else:
                if 'submit_vitals' in data:
                    blood_pressure = data.get('blood_pressure')
                    heart_rate = data.get('heart_rate')
                    body_temperature = data.get('body_temperature')
                    respiratory_rate = data.get('respiratory_rate')
                    oxygen_saturation = data.get('oxygen_saturation')
                    weight = data.get('weight')
                    height = data.get('height')
                    
                    new_vitals = Vitals(blood_pressure=blood_pressure,
                                heart_rate=heart_rate,
                                body_temperature=body_temperature,
                                respiratory_rate=respiratory_rate,
                                oxygen_saturation=oxygen_saturation,
                                weight=weight,
                                height=height)
                    new_vitals.patient_id = patient.id
                    storage.new(new_vitals)

            # Allergies Update
            if allergies:
                allergies.allergen = data.get('allergen', allergies.allergen)
                allergies.reaction = data.get('reaction', allergies.reaction)
                allergies.severity = data.get('severity', allergies.severity)
                allergies.notes = data.get('allergy_notes', allergies.notes)
                allergies.updated_at = datetime.utcnow()
            else:
                if 'submit_allergy' in data:
                    allergen = data.get('allergen')
                    reaction = data.get('reaction')
                    severity = data.get('severity')
                    notes = data.get('allergy_notes')
                    
                    new_allergy = Allergies(allergen=allergen, reaction=reaction,
                                        severity=severity, notes=notes)
                    new_allergy.patient_id = patient.id
                    storage.new(new_allergy)

            # Medical Record Update
            if medical_record:
                medical_record.diagnosis = data.get('diagnosis', medical_record.diagnosis)
                medical_record.treatment = data.get('treatment', medical_record.treatment)
                medical_record.status = data.get('status', medical_record.status)
                medical_record.notes = data.get('medical_record_notes', medical_record.notes)
                medical_record.updated_at = datetime.utcnow()
            else:
                if 'submit_medical_record' in data:
                    diagnosis = data.get('diagnosis')
                    treatment = data.get('treatment')
                    status = data.get('status')
                    notes = data.get('medical_record_notes')
                    
                    new_medical_record = Medical_Record(diagnosis=diagnosis, treatment=treatment,
                                        status=status, notes=notes)
                    new_medical_record.doctor_id = current_user.id
                    new_medical_record.patient_id = patient.id
                    storage.new(new_medical_record)

            # # Appointment Update
            # if appointment:
            #     appointment.appointment_date = data.get('appointment_date', appointment.appointment_date)
            #     appointment.status = data.get('status', appointment.status)
            #     appointment.notes = data.get('notes', appointment.notes)
            #     appointment.updated_at = datetime.utcnow()
            # else:
            #     appointment_date = data.get('appointment_date')
            #     status = data.get('status')
            #     notes = data.get('notes')
                
            #     new_appointment = Appointment(appointment_date=appointment_date, status=status, notes=notes)
            #     new_appointment.doctor_id = current_user.id
            #     new_appointment.patient_id = patient.id
            #     storage.new(new_appointment)

            # Lab Result Update
            if lab_result:
                lab_result.test_name = data.get('test_name', lab_result.test_name)
                lab_result.result = data.get('result', lab_result.result)
                lab_result.values = data.get('values', lab_result.values)
                lab_result.notes = data.get('lab_result_notes', lab_result.notes)
                lab_result.updated_at = datetime.utcnow()
            else:
                if 'submit_lab_result' in data:
                    test_name = data.get('test_name')
                    result = data.get('result')
                    values = data.get('values')
                    notes = data.get('lab_result_notes')
                    
                    new_lab_result = Lab_Results(test_name=test_name, result=result,
                                        values=values, notes=notes)
                    new_lab_result.patient_id = patient.id
                    new_lab_result.doctor_id = current_user.id
                    storage.new(new_lab_result)

            # Medication Update
            if medication:
                medication.medication_name = data.get('medication_name', medication.medication_name)
                medication.dosage = data.get('dosage', medication.dosage)
                medication.frequency = data.get('frequency', medication.frequency)
                medication.start_date = data.get('start_date', medication.start_date)
                medication.end_date = data.get('end_date', medication.end_date)
                medication.prescribing_doctor = data.get('prescribing_doctor', medication.prescribing_doctor)
                medication.notes = data.get('medication_notes', medication.notes)
                medication.updated_at = datetime.utcnow()
            else:
                if 'submit_medication' in data:
                    medication_name = data.get('medication_name')
                    dosage = data.get('dosage')
                    frequency = data.get('frequency')
                    start_date = data.get('start_date')
                    end_date = data.get('end_date')
                    prescribing_doctor = data.get('prescribing_doctor')
                    notes = data.get('medication_notes')
                    
                    new_medication = Medication(medication_name=medication_name, dosage=dosage, frequency=frequency,
                                                start_date=start_date, end_date=end_date,
                                                prescribing_doctor=prescribing_doctor, notes=notes)
                    new_medication.patient_id = patient.id
                    new_medication.doctor_id = current_user.id
                    storage.new(new_medication)

            # Log the access action
            action_taken = (
                    f"{patient.first_name} {patient.last_name}'s records were UPDATED by "
                    f"Doctor {current_user.first_name} {current_user.last_name}"
                    )
            access_log = Access_Log(user_id=current_user.id, patient_id=patient_id, action_taken=action_taken)
            storage.new(access_log)
            storage.save()

            flash('Patient records updated successfully', 'success')
            return redirect(url_for('app_views.update_patient_records', patient_id=patient_id))

        except Exception as e:
            storage._DBStorage__session.rollback() # Rollback the transaction if any error occurs
            abort(500, f"An error occurred while updating records: {str(e)}")


@app_views.route('/doctor/patients/<patient_id>/view_patient_records',
                 methods=['GET'], strict_slashes=False)
@login_required
def view_patient_records(patient_id):
    """Views a patients records based on their ID"""
    if not isinstance(current_user, Doctor):
        abort(403, "You are not authorized to perform this function")

    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(400, "Patient not found")

    vitals = storage.query(Vitals).filter_by(patient_id=patient_id).first()
    medical_record = storage.query(Medical_Record).filter_by(patient_id=patient_id).first()
    allergies = storage.query(Allergies).filter_by(patient_id=patient_id).first()
    appointment = storage.query(Appointment).filter_by(patient_id=patient_id).first()
    lab_result = storage.query(Lab_Results).filter_by(patient_id=patient_id).first()
    medication = storage.query(Medication).filter_by(patient_id=patient_id).first()

    # Log the access action
    action_taken = (
            f"{patient.first_name} {patient.last_name}'s records were VIEWED by "
            f"Doctor {current_user.first_name} {current_user.last_name}"
            )
    access_log = Access_Log(user_id=current_user.id, patient_id=patient_id, action_taken=action_taken)
    storage.new(access_log)
    storage.save()

    return render_template('view_patient_records.html',
                           patient=patient, vitals=vitals,
                           medical_record=medical_record, allergies=allergies,
                           appointment=appointment,lab_result=lab_result,
                           medication=medication)


@app_views.route('/doctor/<doctor_id>/patient/<patient_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_patient(doctor_id, patient_id):
    """Deletes a Patient object based on its ID"""
    doctor = storage.get(Doctor, doctor_id)
    patient = storage.get(Patient, patient_id)

    if not doctor:
        abort(400, "Doctor not found")
    if not patient:
        abort(404, "Patient not found")

    # Log the access
    action_taken = (
        f"{patient.first_name} {patient.last_name}'s record was DELETED by "
        f"Doctor {doctor.first_name} {doctor.last_name}"
        )
    access_log = Access_Log(user_id=doctor_id, patient_id=patient_id, action_taken=action_taken)
    storage.new(access_log)

    # Disable foreign key checks before deleting
    storage._DBStorage__session.execute(text('SET FOREIGN_KEY_CHECKS = 0'))

    # Deletes the Patient
    storage.delete(patient)
    storage.save()

    # Enables foreign key checks after deleting
    storage._DBStorage__session.execute(text('SET FOREIGN_KEY_CHECKS = 1'))
    return jsonify({}), 200
