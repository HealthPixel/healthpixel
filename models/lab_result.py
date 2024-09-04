#!/usr/bin/python3
"""Defines the class Lab Results"""
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Lab_Results(BaseModel, Base):
    """
    Simple model of a Lab Result object

    Attributes:
        patient_id (FK): Foreign Key referencing patient.id
        doctor_id (FK): Foreign Key referencing doctor.id
        test_name (str): Name of the test being conducted
        result (str): Result of the test carried out
        values (text): Values obtained from the test results
        notes (text): Additional notes on the test and results
    """
    __tablename__ = 'lab_results'
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
    test_name = Column(String(100), nullable=False)
    result = Column(String(255), nullable=False)
    values = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
