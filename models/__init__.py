#!/usr/bin/python3
"""This module instantiates the storage object from either FileStorage
or DBStorage
"""
from os import getenv


env = getenv('HBNB_TYPE_STORAGE')
if env == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
