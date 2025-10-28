from app.models.base_model import BaseModel
from app import bcrypt

class User(BaseModel):
    """User class that iherits from BaseModel"""

    def __init__(self, email="", password="", first_name="", last_name="", is_admin=False):
        """Initialize User with provided default attributes"""
        super().__init__()
        self.email = email
        self.password = password_hash # does strore hash password
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    def hash_password(self, password):
        """Hashes the password before storing it"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password"""
        return bcrypt.check_password_hash(self.password, password)

    def get_full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        """Custom string representation"""
        admin_status = " (Admin)" if self.is_admin else ""
        return f"User ({self.id}) {self.email} - {self.get_full_name()}{admin_status}"

    def to_dict(self):
        """Return dictionary representation without password"""
        user_dict = super().to_dict()
        user_dict.update({
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin
        })
        return user_dict
