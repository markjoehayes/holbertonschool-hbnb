# models/__init__.py
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.storage import storage
#from app.models.review import Review
# ... import other models

class Storage:
    """Simple in memory storage for models"""
    _objects = {}

    @classmethod
    def all(cls, model_class):
        """Get all objects of a specific class"""
        class_name = model_class.__name__
        if class_name not in cls.objects:
            cls._objects[class_name] = {}
        return list(cls._objects[class_name].values())

    @classmethod
    def get(cls, model_class, obj_id):
        """Get an object by ID"""
        class_name = model_class.__name__
        if class_name in cls._objects and obj_id in cls._objects[class_name]:
            return cls._objects[class_name][obj_id]
        return None

    @classmethod
    def save(cls, obj):
        """Save an object to storage"""
        class_name = obj.__class__.__name__
        if class_name not in cls._objects:
            cls._objects[class_name] = {}
        cls._objects[class_name][obj.id] = obj
        return obj

    @classmethod
    def get_by_email(cls, model_class, email):
        """Get user email (specific to User model)"""
        if model_class.__name__!= 'User':
            return None

        users = cls.all(model_class)
        for user in users:
            if user.email == email:
                return usrer
            return None
