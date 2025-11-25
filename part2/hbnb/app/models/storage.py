"""A Simple in memory storage class"""

class SimpleStorage:
    def __init__(self):
        self._data = {}
        self._counter = 1

    def new(self, obj):
        """Add a new object to storage"""
        if hasattr(obj, 'id') and not obj.id:
            obj.id = str(self._counter)
            self._counter += 1
        key = f"{obj.__class__.__name__}.{obj.id}"
        self._data[key] = obj

    def get(self, cls, obj_id):
        """Get an object by class and ID"""
        key = f"{cls.__name__}.{obj_id}"
        return self._data.get(key)

    def all(self, cls=None):
        """Get all objects, optionally filtered by class"""
        if cls:
            return {k: v for k, v in self._data.items() if k.startswith(cls.__name__)}
        return self._data

    def save(self):
        """Save objects (in-memory storage doesn't need to persist)"""
        pass

    def delete(self, obj):
        """Delete an object"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        if key in self._data:
            del self._data[key]

# Create a singleton instance
storage = SimpleStorage()
