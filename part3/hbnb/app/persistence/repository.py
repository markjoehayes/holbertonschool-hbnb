from abc import ABC, abstractmethod
from app import db
from app.models.storage import storage  


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass        

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            return obj
        return None

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
    
class InMemoryRepository(Repository):
    def __init__(self):
        """This repository just wraps the global SimpleStorage singleton."""
        pass  # nothing to initialize; all data lives in `storage`

    def add(self, obj):
        """Add an object to the global app storage."""
        print(f"[InMemoryRepository.add] Adding object: id={getattr(obj, 'id', None)}, email={getattr(obj, 'email', None)}")
        try:
            from app.models.storage import storage
            storage.new(obj)
            storage.save()
            print("[InMemoryRepository.add] Successfully saved to storage.")
        except Exception as e:
            import traceback
            print(f"[InMemoryRepository.add] ERROR: {e}")
            print(traceback.format_exc())

    def get(self, obj_id):
        """Retrieve object by ID (any class type)."""
        for obj in storage.all().values():
            if getattr(obj, 'id', None) == obj_id:
                return obj
        return None

    def get_all(self):
        """Return a list of all stored objects."""
        return list(storage.all().values())

    def update(self, obj_id, data):
        """Update attributes and persist."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            storage.save()
        return obj

    def delete(self, obj_id):
        """Delete an object by ID."""
        obj = self.get(obj_id)
        if obj:
            storage.delete(obj)
            storage.save()

    def get_by_attribute(self, attr_name, attr_value):
        """Find the first object matching a given attribute."""
        for obj in storage.all().values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None

