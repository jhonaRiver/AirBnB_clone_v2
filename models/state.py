#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from tkinter import CASCADE
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from models.city import City
import models
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullabe=False)
        cities = relationship('City', backref='state', cascade="all, delete")
    else:
        @property
        def cities(self):
            ''' comment '''
            city_list = []
            for city in models.storage.all(City).values():
                if self.id == city.state_id:
                    city_list.append(city)
            return city_list
