#!/usr/bin/python3
"""
New engine DBStorage
"""

from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = {
        'BaseModel': BaseModel,
        'User': User, 'Place': Place,
        'State': State, 'City': City,
        'Amenity': Amenity, 'Review': Review
        }


class DBStorage:
    """" db storage class """
    __engine = None
    __session = None

    def __init__(self):
        """Engine constructor"""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns query on current database"""
        a_dict = {}
        if cls is None:
            for value in classes.values():
                for o in self.__session.query(value):
                    k = o.__class__.__name__ + '.' + o.id
                    a_dict[k] = o
        if cls in classes:
            for o in self.__session.query(classes[cls]):
                k = o.__class__.__name__ + '.' + o.id
                a_dict[k] = o
        return a_dict

    def new(self, obj):
        """Add object"""
        self.__session.add(obj)

    def save(self):
        """Commit changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads database"""
        Base.metadata.create_all(self.__engine)
        s_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(s_factory)
        self.__session = Session()

    def close(self):
        """Close session"""
        if self.__session is not None:
            self.__session.close()
