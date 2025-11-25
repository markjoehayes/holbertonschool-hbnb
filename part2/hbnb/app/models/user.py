from app.models.base_model import BaseModel

class User(BaseModel):
    """User class that iherits from BaseModel"""

    def __init__(self, email="", password="", first_name="", last_name="", is_admin=False):
        """Initialize User with provided default attributes"""
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    def get_full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        """Custom string representation"""
        admin_status = " (Admin)" if self.is_admin else ""
        return f"User ({self.id}) {self.email} - {self.get_full_name()}{admin_status}"
