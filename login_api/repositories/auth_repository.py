# logindemoapi/repositories/auth_repository.py

from login_api.models import db, User
from sqlalchemy.exc import SQLAlchemyError
from login_api.error_handler.exceptions import DatabaseError



class AuthRepository:
    """
    AuthRepository is responsible for handling authentication-related database operations.
    It interacts with the User model to authenticate users based on their email and password.
    """
    
    def __init__(self, db_session=None):
        """
        Initializes the AuthRepository.
        
        Args:
            db_session: The SQLAlchemy session to use for database operations.
                        Defaults to the global db.session from Flask-SQLAlchemy.
        """
        self.db_session = db_session if db_session is not None else db.session
    
    def authenticate_user(self, email: str, password: str) -> bool:
        """
        Authenticates a user by checking their email and password.
        
        Args:
            email (str): The email of the user.
            password (str): The password of the user.
        
        Returns:
            bool: True if authentication is successful, False otherwise.
        
        Raises:
            DatabaseError: If there is an issue with the database query.
        """
        try:
            user = self.db_session.query(User).filter_by(email=email).first()
            # if user and user.verify_password(password):
            #     return True
            # return False
            if not user or not user.verify_hashed_password(password):
                return False
            return True
        except SQLAlchemyError as e:
            raise DatabaseError(str(e)) from e
