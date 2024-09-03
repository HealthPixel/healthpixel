#!/usr/bin/python3
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.patient import Patient
from models.doctor import Doctor
from models.allergies import Allergies
from models.appointment import Appointment
from models.lab_result import Lab_Results
from models.medical_record import Medical_Record
from models.medication import Medication
from models.vitals import Vitals
from models.access_log import Access_Log


"""Create a storage instance for the application"""
storage = DBStorage()
storage.reload()
