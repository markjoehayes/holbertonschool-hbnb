class InMemoryRepository:
    def __init__(self):
        self._storage = {}
        self._email_index = {}  # For faster email lookups
    
    def add(self, entity):
        """Add a new entity to the repository"""
        if hasattr(entity, 'email'):
            if entity.email in self._email_index:
                raise ValueError(f"Email {entity.email} already exists")
            self._email_index[entity.email] = entity.id
        
        self._storage[entity.id] = entity
    
    def get(self, entity_id):
        """Get an entity by ID"""
        return self._storage.get(entity_id)
    
    def get_by_attribute(self, attr_name, attr_value):
        """Get an entity by a specific attribute"""
        if attr_name == 'email':
            entity_id = self._email_index.get(attr_value)
            return self._storage.get(entity_id) if entity_id else None
        
        for entity in self._storage.values():
            if getattr(entity, attr_name, None) == attr_value:
                return entity
        return None
    
    def list(self):
        """List all entities"""
        return list(self._storage.values())
    
    def update(self, entity_id, update_data):
        """Update an entity"""
        entity = self._storage.get(entity_id)
        if not entity:
            return None
        
        # Handle email updates
        if 'email' in update_data:
            new_email = update_data['email']
            if hasattr(entity, 'email'):
                old_email = entity.email
                if new_email != old_email:
                    if new_email in self._email_index:
                        raise ValueError(f"Email {new_email} already exists")
                    del self._email_index[old_email]
                    self._email_index[new_email] = entity_id
        
        # Update other attributes
        for key, value in update_data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        
        return entity
    
    def delete(self, entity_id):
        """Delete an entity"""
        entity = self._storage.get(entity_id)
        if not entity:
            return False
        
        if hasattr(entity, 'email'):
            del self._email_index[entity.email]
        
        del self._storage[entity_id]
        return True
