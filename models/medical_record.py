#!/usr/bin/python3
"""Defines the class Medical Record"""
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship


class Medical_Record(BaseModel, Base):
    """
    Simple model of a Medical Record object

    Attributes:
        patient_id (FK): Foreign Key referencing patient.id
        doctor_id (FK): Foreign Key referencing doctor.id
        diagnosis (text): The patient's diagnosis
        treatment (text): Details of Doctor's treatment plan
        prescription (text): Prescription given to Patient
        visit_date (datetime): Patient's date for when they were diagnosed
        notes (text): Doctor's notes during the visit
    """
    __tablename__ = 'medical_records'
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
    diagnosis = Column(Text, nullable=False)
    treatment = Column(Text, nullable=False)
    prescription = Column(Text, nullable=False)
    visit_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
