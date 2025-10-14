from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """define the amenity class"""

    def __init__(self, name=""):
        super().__init__()
        self.name = self._validate_name(name)

    def __str__(self):
        """Custom string representation"""
        return f"Amenity ({self.id}) {self.name}" 

    def _validate_name(self, name):
        """Ensure data does not exceed 50 characters"""
        if len(name) > 50:
            raise ValueError("name cannot exceed 50 characters")
        return name
