#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import os
import models

if os.getenv("HBNB_TYPE_STORAGE") == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes a BaseModel instance"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        models.storage.new(self)
        for key in kwargs.keys():
            if key == "__class__":
                continue
            elif key == "created_at" or key == "updated_at":
                setattr(self, key, datetime.fromisoformat(kwargs[key]))
            else:
                setattr(self, key, kwargs[key])

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(self.__class__.__name__,
                                     self.id,
                                     self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__
            of the instance, and adds '__class__' key with value name of class
        """
        new_dict = {}
        new_dict["__class__"] = self.__class__.__name__
        for k, v in self.__dict__.items():
            if type(v) is datetime:
                new_dict[k] = v.isoformat()
            else:
                new_dict[k] = v
        new_dict.pop('_sa_instance_state', None)
        return new_dict

    def delete(self):
        """deletes this object from storage"""
        # TODO: revisit this method
        from models import storage
        storage.delete(self);
