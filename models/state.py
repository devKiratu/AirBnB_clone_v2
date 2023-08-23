#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """Class definition for State, and Mapper class for table states """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

    @property
    def cities(self):
        """getter attribute for use with FileStorage"""
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            from models import storage
            all_objs = storage.all()
            city_objs = []
            for obj in all_objs.items():
                k, v = obj
                if 'City' in k and self.id in v:
                    city_objs.append(obj)

            return city_objs
