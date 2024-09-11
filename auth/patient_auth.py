#!/usr/bin/python3
"""
Creates a new User and Integrates with Backend Database
"""
from models import storage
from models.patient import Patient
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from auth import auth


@auth.route('/logout_patient')
def logout_patient():
    logout_user()
    flash("You have successfully logged out!", 'success')
    return render_template('login.html')


@auth.route('/patient_dashboard/<id>')
@login_required
def dashboard_patient(id):
    user_data = storage._DBStorage__session.query(Patient).filter_by(id=current_user.id).first()
    if current_user.id != id:
        return render_template('error.html', message='Unauthorized access.')

    return render_template('patient_dashboard.html', user=user_data, user_id=id)


@auth.route('/patient_dashboard')
@login_required
def dashboard_redirect_patient():
    # Redirect to the current user's dashboard using their ID
    return redirect(url_for('auth.dashboard_patient', id=current_user.id))


# @auth.route('/delete_doctor', methods=['GET'])
# def delete_doctor():
#     delete_doc_api_url = f"http://127.0.0.1:5000/api/v1/doctor/{current_user.id}"
#     response = requests.delete(delete_doc_api_url)
#     del_success = "Your account has been deleted successfully!"
#     return redirect(url_for('auth.login', del_success=del_success))
