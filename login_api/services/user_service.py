# logindemoapi/services/user_service.py

from typing import Optional
from login_api.repositories.user_repository import UserRepository
# For password hashing (install Flask-Bcrypt or passlib if not already)
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt() # Initialize in app.py and pass to service if needed more broadly

class UserService:
    """
    UserService encapsulates the business logic for User-related operations.
    It interacts with the UserRepository and orchestrates transactions.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
        # If you need Bcrypt here for hashing, pass it in init or import locally
        # self.bcrypt = bcrypt_instance

    def create_user(self, email: str, password: str, first_name: str, last_name: str, is_active: bool) -> dict:
        """
        Creates a new user, applies business rules, and saves to the database.

        Args:
            email (str): The email for the new user.
            password (str): The plain text password (will be hashed).
            first_name (str): The first name of the new user.
            last_name (str): The last name of the new user.
            is_active (bool): Whether the user account is active.

        Returns:
            dict: A dictionary representation of the newly created user.

        Raises:
            ValueError: If a user with the given email already exists,
                        or if other business rules are violated.
            RuntimeError: For unexpected database errors.
        """
        # Business Rule: Check if email already exists
        # Although handled by IntegrityError in repo, explicit check can give clearer messages
        if self.user_repo.get_by_email(email):
            raise ValueError(f"Email '{email}' already registered.")

        # Business Rule: Password Hashing
        # In a real app, use a proper hashing library
        # hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        hashed_password = f"hashed_{password}_service" # Placeholder for real hashing

        try:
            # Delegate to repository
            new_user = self.user_repo.add(email, 
                                          hashed_password, 
                                          first_name,
                                          last_name,
                                          is_active)
            self.user_repo.db_session.commit() # Commit the transaction here!
            return new_user.to_dict() # Return a dictionary for the controller
        except ValueError as e: # Catch specific ValueError from repository
            raise # Re-raise if it's a business logic error
        except RuntimeError as e: # Catch specific RuntimeError from repository
            raise # Re-raise for unexpected database errors
        except Exception as e:
            self.user_repo.db_session.rollback() # Rollback on any unexpected error
            raise RuntimeError(f"An unexpected error occurred during user creation: {e}") from e

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """Retrieves a user by ID."""
        user = self.user_repo.get_by_id(user_id)
        return user.to_dict() if user else None

    def get_all_users(self) -> list[dict]:
        """Retrieves all users."""
        users = self.user_repo.get_all()
        return [user.to_dict() for user in users]

    def update_user(self, user_id: int, 
                    first_name: Optional[str] = None,
                    last_name: Optional[str] = None) -> dict:
        """
        Updates an existing user with new data.
    
        Args:
            user_id (int): The ID of the user to update.
            first_name (Optional[str]): New first name for the user.
            last_name (Optional[str]): New last name for the user.
    
        Returns:
            dict: The updated user data.
    
        Raises:
            ValueError: If the user does not exist
            RuntimeError: For unexpected database errors.
        """
        # Fetch existing user
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist.")
    
        # Update fields if provided
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        
        try:
            self.user_repo.update(user)
            self.user_repo.db_session.commit()  # Commit the transaction here!
            return user.to_dict()
        except ValueError as e:
            raise # Re-raise if it's a business logic error
        except RuntimeError as e:
            raise # Re-raise for unexpected database errors
        except Exception as e:
            self.user_repo.db_session.rollback() # Rollback on any unexpected error
            raise RuntimeError(f"An unexpected error occurred during user creation: {e}") from e
        
    def delete_user(self, user_id: int) -> None:
        """
        Deletes a user by ID.
    
        Args:
            user_id (int): The ID of the user to delete.
    
        Raises:
            ValueError: If the user does not exist.
            RuntimeError: For unexpected database errors.
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist.")
        
        try:
            self.user_repo.delete(user)
            self.user_repo.db_session.commit()  # Commit the transaction here!
        except ValueError as e:
            raise # Re-raise if it's a business logic error
        except RuntimeError as e:
            raise # Re-raise for unexpected database errors
        except Exception as e:
            self.user_repo.db_session.rollback() # Rollback on any unexpected error
            raise RuntimeError(f"An unexpected error occurred during user deletion: {e}") from e