#!/usr/bin/python3
"""Defines the class Medication"""
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship


class Medication(BaseModel, Base):
    """
    Simple model of a Medication object

    Attributes:
        patient_id (str): Foreign Key referencing patient.id
        doctor_id (str): Foreign Key referencing doctor.id
        medication_name (str): Name of the prescribed medicine
        dosage (str): Dosage of the medication
        frequency (str): Frequency of administration (e.g., once daily)
        start_date (date): Date for which the patient should start taking medication
        end_date (date): Date for which the patient should be done with the medication
        prescribing_doctor (str): Name of the doctor prescribing the medication
        notes (text): Doctor's notes on the medication
    """
    __tablename__ = 'medications'

    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
    medication_name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    prescribing_doctor = Column(String(100), nullable=False)
    notes = Column(Text, nullable=True)
