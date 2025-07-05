# logindemoapi/repositories/user_repository.py

from typing import Optional
from login_api.models import db, User # Relative import from logindemoapi.models
# IntegrityError: for handling unique constraints etc.
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from login_api.error_handler.user_exceptions import UserNotFoundError, UserAlreadyExistsError
from login_api.error_handler.exceptions import DatabaseError


class UserRepository:
    """
    UserRepository handles all database interactions related to the User entity.
    It acts as an abstraction layer between the service layer and the database.
    """

    def __init__(self, db_session=None):
        """
        Initializes the UserRepository.
        Args:
            db_session: The SQLAlchemy session to use for database operations.
                        Defaults to the global db.session from Flask-SQLAlchemy.
        """
        self.db_session = db_session if db_session is not None else db.session

    def add(self, email: str, password_hash: str, first_name: str, last_name: str, is_active: bool) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The email of the new user.
            password_hash (str): The hashed password of the new user.
            first_name (str): The first name of the new user.
            last_name (str): The last name of the new user.
            is_active (bool): Whether the user account is active.

        Returns:
            User: The newly created User object.

        Raises:
            IntegrityError: If a unique constraint is violated (e.g., duplicate email).
            Exception: For other database-related errors.
        """
        try:
            new_user = User(email=email, 
                            password_hash=password_hash, 
                            first_name=first_name,
                            last_name=last_name,
                            is_active=is_active)
            self.db_session.add(new_user)
            # No commit here! The service layer will handle transactions.
            self.db_session.flush() # Flush to get the ID if needed immediately (e.g., for related objects)
            return new_user
        except IntegrityError as e:
            self.db_session.rollback()
            raise UserAlreadyExistsError()
        except SQLAlchemyError as e:
            raise DatabaseError(str(e)) from e

    def get_by_id(self, user_id: int) -> User:
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The User object if found.
        
        Raises:
            UserNotFoundError: If no user with the given ID exists.
            DatabaseError: For any database-related errors.
        """
        try:
            user = self.db_session.get(User, user_id)
            if not user:
                raise UserNotFoundError()
            return user
        except SQLAlchemyError as e:
            raise DatabaseError(str(e)) from e

    # Used by create_user in user_service.py
    # This method is used to check if a user with the given email already exists.
    def get_by_email(self, email: str) -> User:
        """
        Retrieves a user by their email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            User: The User object if found.
        
        Raises:
            UserNotFoundError: If no user with the given email exists.
            DatabaseError: For any database-related errors.
        """
        try:
            user = self.db_session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
            if not user:
                raise UserNotFoundError()
            return user
        except SQLAlchemyError as e:
            raise DatabaseError(str(e)) from e

    def get_all(self) -> list[User]:
        """
        Retrieves all users.

        Args:
            None
        
        Returns:
            list[User]: A list of all User objects in the database.
        
        Raises:
            DatabaseError: For any database-related errors.
        """
        try:
            # Using scalars() to get a list of User objects directly
            return self.db_session.execute(db.select(User)).scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError(str(e)) from e

    def update(self, user: User) -> User:
        """
        Updates an existing user in the database.
        
        Args:
            user (User): The User object with updated data.

        Returns:
            User: The updated User object.

        Raises:
            UserNotFoundError: If the user does not exist.
            DatabaseError: For any database-related errors.
        """
        try:
            existing_user = self.get_by_id(user.id)
            if not existing_user:
                raise UserNotFoundError()
        
            self.db_session.add(existing_user)
            self.db_session.flush()
            return existing_user
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise DatabaseError(str(e)) from e
    
    def delete(self, user: User):
        """
        Deletes a user from the database.

        Args:
            user (User): The User object to delete.

        Returns:
            None
        
        Raises:
            UserNotFoundError: If the user does not exist.
            DatabaseError: For any database-related errors.
        """
        try:
            existing_user = self.get_by_id(user.id)
            if not existing_user:
                raise UserNotFoundError()
            self.db_session.delete(user)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise DatabaseError(str(e)) from e
