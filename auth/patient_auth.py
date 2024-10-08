#!/usr/bin/python3
"""
Creates a new User and Integrates with Backend Database
"""
from models import storage
from models.patient import Patient
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
import requests
from auth import auth
from models.medication import Medication


@auth.route('/logout_patient')
def logout_patient():
    logout_user()
    flash("You have successfully logged out!", 'success')
    return render_template('login.html')


@auth.route('/patient_dashboard/<id>')
@login_required
def dashboard_patient(id):
    user_data = storage._DBStorage__session.query(Patient).filter_by(id=current_user.id).first()
    medication = storage.query(Medication).filter_by(patient_id=id).first()
    if current_user.id != id:
        return render_template('error.html', message='Unauthorized access.')

    return render_template('patient_dashboard.html', user=user_data, user_id=id, medication=medication)


@auth.route('/patient_dashboard')
@login_required
def dashboard_redirect_patient():
    # Redirect to the current user's dashboard using their ID
    return redirect(url_for('auth.dashboard_patient', id=current_user.id))


@auth.route('/delete_patient/<patient_id>', methods=['GET'])
def delete_patient(patient_id):
    delete_pat_api_url = f"http://127.0.0.1:5000/api/v1/doctor/{current_user.id}/patient/{patient_id}"
    response = requests.delete(delete_pat_api_url)
    flash("Patient account has been deleted successfully!", 'success')
    return redirect(url_for('auth.dashboard_doctor', id=current_user.id))
