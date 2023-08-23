#!/usr/bin/python3
"""Defines engine for interacting with database"""

from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """class definition for db storage engine"""
    __enigne = None
    __session = None

    def __init__(self):
        """initialize engine"""
        # dialect+driver://username:password@host:port/database
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'
                .format(user, pwd, host, db), pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def all(self, cls=None):
        """query on the current database session (self.__session) all
        objects depending of the class name (argument cls)
        """
        objs = {}
        if cls is None:
            cls_objects = {
                    'State': State,
                    'City': City,
                    'User': User,
                    'Place': Place,
                    'Review': Review
                    }
        else:
            print(f"=== cls passed to all {cls} ===")
            cls_objects = [cls]
        for key in cls_objects.keys():
            rows = self.__session.query(cls_objects[key]).all()
            # print(f" ===== rows: {rows} ======")
            for row in rows:
                # print(f" ======= {key.split('.')[0]}: {key} ====== ")
                key = f"{key.split('.')[0]}.{cls_objects[key.split('.')[0]]}"
                objs[key] = row
        return objs

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
