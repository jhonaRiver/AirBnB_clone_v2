#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import models
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        name = ''

        @property
        def cities(self):
            '''
            Getter attribute
            '''
            cities_in_state = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    cities_in_state.append(city)
            return cities_in_state
