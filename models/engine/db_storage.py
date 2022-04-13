#!/usr/bin/python3
''' STORAGE for when the Engine is based on SQL '''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review
import os


class DBStorage:
    ''' Database storage class '''
    __engine = None
    __session = None
    hbnb_classes = {
        'BaseModel': BaseModel,
        'City': City, 'User': User,
        'Place': Place, 'State': State,
        'Amenity': Amenity, 'Review': Review
    }

    def __init__(self):
        ''' DataBase Storage Constructor '''
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        query on the current database session
        all objects depending of the class name
        '''
        newdict = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                newdict[str(cls) + "." + obj.id] = obj
        else:
            for key, value in self.hbnb_classes.items():
                try:
                    query = self.__session.query(value).all()
                except:
                    pass
                for obj in query:
                    newdict[key + "." + obj.id] = obj

        return newdict

    def new(self, obj):
        ''' add the object to the current database session '''
        self.__session.add(obj)

    def delete(self, obj=None):
        ''' delete from the current database session obj if not None '''
        if obj is not None:
            self.__session.delete(obj)

    def save(self):
        '''  commit all changes of the current database session '''
        self.__session.commit()

    def reload(self):
        ''' create all tables in the database (feature of SQLAlchemy) '''
        Base.metadata.create_all(self.__engine)
        # creates a new session
        s_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # creates a new object
        Session = scoped_session(s_factory)

        # Is an instanced of the session which can be used to talk to the DB
        self.__session = Session()

    def close(self):
        if self.__session is not None:
            self.__session.close()
