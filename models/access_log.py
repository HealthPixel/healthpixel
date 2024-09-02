#!/usr/bin/python3
"""Defines the Access_Log class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime


class Access_Log(BaseModel, Base):
    """
    Logs access to patient records

    Attributes:
        user_id (str): ID of the user who accessed the record (doctor)
        patient_id (str): ID of the patient whose record was accessed
        accessed_at (datetime): Timestamp of when the access occurred
    """
    __tablename__ = 'access_logs'
    user_id = Column(String(60), ForeignKey('doctors.id'), nullable=False)
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
