#!/usr/bin/python3
"""Defines the class Vitals"""
import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float


class Vitals(BaseModel, Base):
    """
    Simple model of a Vitals object

    Attributes:
        patient_id (str): Foreign Key referencing patient.id
        blood_pressure (str): Patient's blood pressure (e.g., 120/80 mmHg)
        heart_rate (int): Patient's heart rate (beats per minute)
        body_temperature (float): Patient's body temperature (°C)
        respiratory_rate (int): Patient's respiratory rate (breaths per minute)
        oxygen_saturation (float): Patient's oxygen saturation level (%)
        weight (float): Patient's weight (kg)
        height (float): Patient's height (meters)
    """
    __tablename__ = 'vitals'

    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    blood_pressure = Column(String(50), nullable=False)  # E.g: "120/80 mmHg"
    heart_rate = Column(Integer, nullable=False)  # Beats per minute
    body_temperature = Column(Float, nullable=False)  # Celsius
    respiratory_rate = Column(Integer, nullable=False)  # Breaths per minute
    oxygen_saturation = Column(Float, nullable=False)  # Percentage (%)
    weight = Column(Float, nullable=False)  # Kilograms (kg)
    height = Column(Float, nullable=False)  # Meters (m)
