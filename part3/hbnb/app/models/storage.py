# app/models/storage.py
"""A simple in-memory storage singleton with a small API expected by the app."""

import threading

class SimpleStorage:
    def __init__(self):
        # use a dict keyed by "<ClassName>.<id>"
        self._data = {}
        # simple counter for numeric ids (if some models rely on it)
        self._counter = 1
        # tiny lock so concurrent requests don't clobber the dict
        self._lock = threading.Lock()

    def new(self, obj):
        """Add a new object to storage. Assigns an id if missing/empty."""
        with self._lock:
            if hasattr(obj, 'id') and not obj.id:
                obj.id = str(self._counter)
                self._counter += 1
            key = f"{obj.__class__.__name__}.{obj.id}"
            self._data[key] = obj
        return obj

    def get(self, cls, obj_id):
        """Get an object by class and ID. cls can be class object or class name."""
        cname = cls.__name__ if not isinstance(cls, str) else cls
        key = f"{cname}.{obj_id}"
        return self._data.get(key)

    def all(self, cls=None):
        """Return all objects or only objects of a given class."""
        if cls:
            cname = cls.__name__ if not isinstance(cls, str) else cls
            return {k: v for k, v in self._data.items() if k.startswith(cname + ".")}
        # return the dict (not a copy) because callers expect to iterate values()
        return self._data

        def get_by_email(self, cls, email):
            """Find a user by email (specific to User)."""
            cname = cls.__name__ if not isinstance(cls, str) else cls
            for k, v in self._data.items():
                if k.startswith(cname + ".") and getattr(v, "email", None) == email:
                    return v
            return None


    def delete(self, obj):
        """Delete an object instance."""
        with self._lock:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self._data:
                del self._data[key]

    def save(self):
        """
        Persist changes.
        For current in-memory implementation this is a no-op (keeps behavior consistent).
        If later you add file or DB persistence, implement it here.
        """
        # no-op for in-memory simple storage
        return

# singleton instance used by the rest of the app
storage = SimpleStorage()

