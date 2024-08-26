#!/usr/bin/python3
"""
This module contains a Base class defining all common attributes/methods
for other classes
"""
import models
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """
    This is the base class that defines all common attributes/methods
    for other classes
    """
    id = Column(String(60), nullable=False, primary_key=True,
                default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initializes the class with public instance attributes

        Attributes:
        id: assigned with uuid to provide a unique id for each BaseModel
            instance created
        created_at: uses datetime to assign the current datetime when an
            instance is created
        updated_at: uses datetime to assign the current datetime when an
            instance is created & updated everytime the object is changed
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """Returns the string representation of BaseModel instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Public instance method that updates the public instance attribute
        'updated_at' with the current time
        """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Public instance method that returns a dictionary containing all
        key/value pairs of __dict__ of the instance
        """
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary:
            dictionary.pop("_sa_instance_state")
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage"""
        from models import storage
        storage.delete(self)
