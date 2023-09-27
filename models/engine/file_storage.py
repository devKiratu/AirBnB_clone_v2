#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a list of objects of one type of class"""
        if cls is None:
            return self.__objects
        cls_objs = {}
        for k, v in self.__objects.items():
            if v.__class__ == cls:
                cls_objs[k] = v
        return cls_objs

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        for item in self.__objects:
            temp[item] = self.__objects[item].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.__objects[key] = classes[key['__class__']](**val)
        except Exception:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects"""
        if obj is not None:
            cls_name = obj.__class__.__name__
            obj_key = f"{cls_name}.{obj.id}"
            del self.__objects[obj_key]

    def close(self):
        """
        calls the `reload` method for deserializing the JSON file to
        objects
        """
        self.reload()
