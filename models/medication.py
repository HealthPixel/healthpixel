#!/usr/bin/python3
"""Defines the class Medication"""
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text


class Medication(BaseModel, Base):
    """
    Simple model of a Medication object

    Attributes:
        patient_id (str): Foreign Key referencing patient.id
        doctor_id (str): Foreign Key referencing doctor.id
        medicine_name (str): Name of the prescribed medicine
        dosage (str): Dosage of the medication
        frequency (str): Frequency of administration (e.g., once daily)
        duration (str): Duration for which the medication should be taken
        notes (text): Doctor's notes on the medication
    """
    __tablename__ = 'medications'

    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
    medicine_name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    duration = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)
