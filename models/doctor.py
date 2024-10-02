#!/usr/bin/python3
"""Defines the class Doctor"""
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app


class Doctor(BaseModel, Base, UserMixin):
    """
    Simple model of a Doctor object

    Attributes:
        first_name (str): First name of the Doctor
        last_name (str): Last name of the Doctor
        phone_number (str): Phone number of the Doctor
        email (str): Email address of the Doctor
        specialization (str): Doctor's specialization
    """
    __tablename__ = 'doctors'
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    specialization = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)


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
