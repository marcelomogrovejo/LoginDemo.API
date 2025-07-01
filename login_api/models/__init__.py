# logindemoapi/models/__init__.py

from login_api.extensions import db
# Import all your models here
from .user_model import User  # Example

__all__ = ['User', 'db']  # Explicit exports