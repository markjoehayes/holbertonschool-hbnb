from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid

# THIS MUST EXIST — SQLAlchemy Base for all tables
Base = declarative_base()

class BaseModel(Base):
    """Base class for all SQLAlchemy models."""
    __abstract__ = True   # <-- do NOT create a table for BaseModel

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def to_dict(self, include_password=False):
        """Convert SQLAlchemy object into dict."""
        d = {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        return d

    def save(self, session):
        """Save object and update timestamps."""
        self.updated_at = datetime.utcnow()
        session.add(self)

