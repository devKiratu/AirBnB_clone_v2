#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
import os


class Amenity(BaseModel, Base):
    """Mapper class for Amenity"""
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes the Amenity class"""
        super().__init__(*args, **kwargs)
