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

#    def save(self):
#        """
#        Persist changes.
#        For current in-memory implementation this is a no-op (keeps behavior consistent).
#        If later you add file or DB persistence, implement it here.
#        """
        # no-op for in-memory simple storage
#        return

# singleton instance used by the rest of the app
#storage = SimpleStorage()
    def save(self):
        """Persist the in-memory _data to a JSON file."""
        import json
        from app.models.user import User

        try:
            json_data = {}
            for key, obj in self._data.items():
                # Prefer to_dict() for serializable form
                if hasattr(obj, "to_dict"):
                    json_data[key] = obj.to_dict(include_password=True)
                else:
                    json_data[key] = obj.__dict__

            with open("simple_storage.json", "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
            print(f"[SimpleStorage.save] Saved {len(json_data)} objects to simple_storage.json")
        except Exception as e:
            print(f"[SimpleStorage.save] ERROR: {e}")
    
#    def reload(self):
#        """Load objects from JSON file back into memory."""
#        import json
#        import os
#        from app.models.user import User
#
#        filepath = "simple_storage.json"
#        if not os.path.exists(filepath):
#            print("[SimpleStorage.reload] No existing file, starting fresh")
#        return

#        try:
#            with open(filepath, "r", encoding="utf-8") as f:
#                data = json.load(f)

#            count = 0
#            for key, obj_dict in data.items():
#                cls_name = obj_dict.get("__class__")
#                if cls_name == "User":
                    # Recreate user instance
#                    obj = User(**{
#                        "id": obj_dict.get("id"),
#                        "first_name": obj_dict.get("first_name"),
#                        "last_name": obj_dict.get("last_name"),
#                        "email": obj_dict.get("email"),
#                        "password": obj_dict.get("password"),
#                        "is_admin": obj_dict.get("is_admin", False),
#                        "created_at": obj_dict.get("created_at"),
#                        "updated_at": obj_dict.get("updated_at")
#                    })
#                    self._data[key] = obj
#                    count += 1
#            print(f"[SimpleStorage.reload] Loaded {count} objects from {filepath}")
#        except Exception as e:
#            print(f"[SimpleStorage.reload] ERROR: {e}")

    def reload(self):
        """Load data back from JSON into memory"""
        import json
        try:
            with open("simple_storage.json", "r", encoding="utf-8") as f:
                json_data = json.load(f)

            for key, value in json_data.items():
                cls_name = value.get("__class__")
                if cls_name == "User":
                    from app.models.user import User
                    obj = User(
                        email=value.get("email"),
                        password=value.get("password"),  # stays hashed
                        first_name=value.get("first_name"),
                        last_name=value.get("last_name"),
                        is_admin=value.get("is_admin", False),
                    )   
                    obj.id = value.get("id")
                    obj.created_at = value.get("created_at")
                    obj.updated_at = value.get("updated_at")
                    self._data[key] = obj
        except FileNotFoundError:
            print("[SimpleStorage.reload] No file found yet")

# Singleton instance used by the rest of the app
storage = SimpleStorage()
storage.reload()

