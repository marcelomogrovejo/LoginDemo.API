# logindemoapi/models/user_model.py

from login_api.extensions import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), 
                          default=lambda: datetime.now(timezone.utc), 
                          nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), 
                          default=lambda: datetime.now(timezone.utc),
                          onupdate=lambda: datetime.now(timezone.utc),
                          nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        """Converts the User object to a dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def verify_password(self, password: str) -> bool:
        """
        Verifies the provided password against the stored password hash.
        
        Args:
            password (str): The password to verify.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        # Placeholder for real password verification logic
        return self.password_hash == f"hashed_{password}_service"