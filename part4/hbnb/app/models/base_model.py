from app import db
import uuid
from datetime import datetime

#class BaseModel:
#    """Defines all common attributes/methods for other classes"""
#
#    def __init__(self):
#        """Initializes the base model"""
#        self.id = str(uuid.uuid4())
#        self.created_at = datetime.now()
#        self.updated_at = datetime.now()
#
#    def __str__(self):
#        """String Rep"""
#        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
#
#    def save(self):
#        """Update the updated_at timestamp whenever the object is modified"""
#        self.updated_at = datetime.now()
#
#    def update(self, data):
#        """Update the attributes of the object based on the provided dictionary"""
#        for key, value in data.items():
#            if hasattr(self, key):
#                setattr(self, key, value)
#        self.save()  # Update the updated_at timestamp
#
#    def to_dict(self, include_password=False):
#        """Convert the object to a dictionary for serialization"""
#        obj_dict = self.__dict__.copy()
#        obj_dict['__class__'] = self.__class__.__name__
#
#        if "created_at" in obj_dict and isinstance(obj_dict["created_at"], datetime):
#            obj_dict["created_at"] = obj_dict["created_at"].isoformat()
#        if "updated_at" in obj_dict and isinstance(obj_dict["updated_at"], datetime):
#            obj_dict["updated_at"] = obj_dict["updated_at"].isoformat()
#
#        # Exclude password by default unless explicitly requested
#        if not include_password and 'password' in obj_dict:
#            obj_dict.pop('password', None)
#        obj_dict['created_at'] = self.created_at.isoformat()
#        obj_dict['updated_at'] = self.updated_at.isoformat()
#        return obj_dict 

class BaseModel(db.Model):
    __abstract__ = True  # no table for this class

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_password=False):
        """Return a dict representation of the model."""
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if not include_password and "password" in data:
            del data["password"]
        return data

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

