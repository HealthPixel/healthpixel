#!/usr/bin/python3
"""
This file defines a new engine for DataBase Storage
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.patient import Patient
from models.doctor import Doctor
from models.allergies import Allergies
from models.appointment import Appointment
from models.lab_result import Lab_Results
from models.medical_record import Medical_Record
from models.medication import Medication
from models.vitals import Vitals
from models.access_log import Access_Log


class DBStorage():
    """Defines the database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """
        Creates the engine and links it to the MySQL database
        and user
        """
        env = getenv("HP_ENV")
        user = getenv("HP_MYSQL_USER")
        password = getenv("HP_MYSQL_PWD")
        host = getenv("HP_MYSQL_HOST")
        db = getenv("HP_MYSQL_DB")
        db_url = f"mysql+mysqldb://{user}:{password}@{host}/{db}"

        self.__engine = create_engine(db_url)
    
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session and return a dictionary
        """
        if cls is None:
            my_classes = Base.__subclasses__()
        else:
            my_classes = [cls]

        result = {}
        for my_class in my_classes:
            objects = self.__session.query(my_class).all()
            for obj in objects:
                key = f"{obj.__class__.__name__}.{obj.id}"
                result[key] = obj
        return result

    def new(self, obj):
        """Adds an object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def get_session(self):
        return self.__session

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)

        """
        self.__session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        """
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """Closes the session"""
        self.__session.remove()

    def query(self, cls):
        """Helper method for querying the database"""
        return self.__session.query(cls)

    def get(self, cls, id):
        """
        A method to retrieve one object
        Args:
            cls - Class
            id - String representing the object ID
        """
        result = self.__session.query(cls).filter_by(id=id).first()
        return result
