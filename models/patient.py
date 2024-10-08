#!/usr/bin/python3
"""Defines the class Patient"""
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer


class Patient(BaseModel, Base, UserMixin):
    """
    Simple model of a Patient object

    Attributes:
        first_name (str): First name of the Patient
        last_name (str): Last name of the Patient
        date_of_birth (date): Date of birth of the Patient
        gender (str): Gender of the Patient
        blood_group (str): Blood group of the Patient
        address (str): Address of the Patient
        zipcode (str): Zipcode of the Patient's address
        phone_number (str): Phone number of the Patient
        email (str): Email of the Patient
        emergency_contact (str): Emergency contact details of the Patient
                                 (name & phone number)
    """
    __tablename__ = 'patients'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(30), nullable=False)
    address = Column(String(255), nullable=True)
    zipcode = Column(String(20), nullable=True)
    password = Column(String(128), nullable=False)
    blood_group = Column(String(20), nullable=False)
    emergency_contact_name = Column(String(50), nullable=False)
    emergency_contact_phone = Column(String(50), nullable=False)


    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        from models import storage

        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        return storage.query(Doctor).get(user_id)
