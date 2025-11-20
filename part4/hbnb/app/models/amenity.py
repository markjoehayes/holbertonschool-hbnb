from app import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """define the amenity class"""

    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    # relationship to Place (if a place can have amenities)
    places = db.relationship(
        "Place",
         secondary="place_amenities",  # through association table
         back_populates="amenities"
    )

    def __init__(self, name="", description=""):
        super().__init__()
        self.name = name
        self.description = description

    def _validate_name(self, name):
        """Ensure data does not exceed 50 characters"""
        if len(name) > 50:
            raise ValueError("name cannot exceed 50 characters")
        return name

    def __repr__(self):
        return f"<Amenity {self.id}: {self.name}>"

