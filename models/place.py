#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
import models
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey, String, Float, Column, Integer, Table
from sqlalchemy.orm import relationship


if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref='place',
                           cascade='all, delete, delete-orphan')
    amenities = relationship("Amenity", secondary='place_amenity',
                            viewonly=False)
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """Getter"""
            review_list = []
            all_reviews = models.storage.all(Review)
            for rev in all_reviews.values():
                if self.id == rev.place_id:
                    review_list.append(rev)
            return review_list

        @property
        def amenities(self):
            """Getter"""
            amenities_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.id == self.amenity_ids:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, value):
            """
            Setter
            """
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
