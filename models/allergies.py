#!/usr/bin/python3
"""Defines the class Allergies"""
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Allergies(BaseModel, Base):
    """
    Simple model of an Allergies object

    Attributes:
        patient_id (FK): Foreign Key referencing patient.id
        allergy (str): The Patient's allergy
        reaction (text): The Patient's reaction caused by the allergy
        severity (text): How severe the Allergic reaction is
        notes (text): Doctor's notes on the Patient's allergy
    """
    __tablename__ = 'allergies'
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    allergen = Column(String(50), nullable=True)
    reaction = Column(Text, nullable=True)
    severity = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
