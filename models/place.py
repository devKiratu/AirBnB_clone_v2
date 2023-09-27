#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import os


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
            'place_amenity', Base.metadata,
            Column('place_id', String(60), ForeignKey('places.id'),
                   primary_key=True, nullable=False),
            Column('amenity_id', String(60), ForeignKey('amenities.id'),
                   primary_key=True, nullable=False)
            )


class Place(BaseModel, Base):
    """ Mapper class for table places"""
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
        amenities = relationship("Amenity", secondary='place_amenity',
                                 backref="place_amenities", viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initialize the Place class"""
        super().__init__(*args, **kwargs)

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        from models import storage
        from models.review import Review
        from models.amenity import Amenity

        @property
        def reviews(self):
            """getter attribute for use with FileStorage"""
            all_reviews = storage.all(Review).values()
            required_reviews = []
            for review in all_reviews:
                if review.place_id == self.id:
                    required_reviews.append(review)
            return review_objs

        @property
        def amenities(self):
            """getter attribute for use with FileStorage"""
            all_amenities = storage.all(Amenity).values()
            required_amenities = []
            for amenity in all_amenities:
                if amenity.place_id == self.id:
                    required_amenities.append(amenity)
            return required_amenities
