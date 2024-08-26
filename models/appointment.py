#!/usr/bin/python3
"""Defines the class Appointment"""
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship


class Appointment(BaseModel, Base):
    """
    Simple model of an Appointment object

    Attributes:
        patient_id (FK): Foreign Key referencing patient.id
        doctor_id (FK): Foreign Key referencing doctor.id
        appointment_date (datetime): Patient's appointment date
        status (str): Appointment's status (Scheduled, Completed, Cancelled)
        notes (text): Doctor's notes during the appointment
    """
    __tablename__ = 'appointments'
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)
    notes = Column(Text, nullable=True)
