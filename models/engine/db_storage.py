#!/usr/bin/python3
''' Module defining DBStorage class '''

import MySQLdb
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class DBStorage:
    __engine = None
    __session = None

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City
    }

    def __init__(self, user=None, passwd=None, host=None, db=None):

        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, passwd, host, db),
            pool_pre_ping=True)

    def all(self, cls=None):
        ''' IN BETA '''
        cls_dict = {}
        if cls:
            db = self.__session.query(cls).all()
            for obj in db:
                cls_dict[str(cls) + "." + obj.id] = obj
        else:
            for key, value in self.hbnb_classes.items():
                try:
                    db = self.__session.query(value).all()
                except:
                    pass
                for obj in db:
                    cls_dict[key + "." + obj.id] = obj

        return cls_dict

    def new(self, obj):
        ''' add object to current db '''
        print(obj)
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        ''' commit changes of current db '''
        self.__session.commit()

    def delete(self, obj=None):
        ''' delete current db '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        ''' create all tables in the db from the engine '''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        ''' close the session'''
        if self.__session is not None:
            self.__session.close()
