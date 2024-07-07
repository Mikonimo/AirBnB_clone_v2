#!/usr/bin/python3
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os
"""This module contains the DataBase Storage"""


class DBStorage:
    """Manages the Database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the Database"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine(
           f'mysql+mysqldb://{user}:{password}@{host}/{database}',
           pool_pre_ping=True
        )
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for cls in Base.__subclasses__():
                objs.extend(self.__session.query(cls).all())
        return {obj.__class__.__name__ + '.' + obj.id: obj for obj in objs}

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not none"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the session"""
        from models.city import City
        from models.state import State
        from models.user import User
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
