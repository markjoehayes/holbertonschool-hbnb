from app.models.base_model import BaseModel
from app import db, bcrypt

class User(BaseModel):
    """User class that inherits from BaseModel"""
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # relatiionships
    places = db.relationship("Place", back_populates="owner", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")



    def __init__(self, **kwargs):
        """Initialize the User and hash password if provided."""
        password = kwargs.pop("password", None)
        super().__init__(**kwargs)

#    def __init__(self, email="", password="", first_name="", last_name="", is_admin=False):
#        """Initialize User with provided default attributes"""
#
#        super().__init__()
#        self.email = email
#        self.first_name = first_name
#        self.last_name = last_name
#        self.is_admin = is_admin
        # hash the password if provided and not already hashed
        if password:
            # check if already hashed - starts with $2b$
            if password.startswith('$2b$'):
                self.password = password
            else:
                self.hash_password(password)
        else:
            self.password = ""

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

#    def to_dict(self):
#        """Return dictionary representation without password"""
#        user_dict = super().to_dict()
#        if 'password' in user_dict:
#            del user_dict['password']
#        user_dict.update({
#            'email': self.email,
#            'first_name': self.first_name,
#            'last_name': self.last_name,
#            'is_admin': self.is_admin
#        })
#        return user_dict

    def to_dict(self, include_password=False):
        """Return a dictionary representation of the User."""
        data = super().to_dict(include_password=include_password)
        data.update({
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin
        })
        if include_password:
            data["password"] = self.password
        return data

