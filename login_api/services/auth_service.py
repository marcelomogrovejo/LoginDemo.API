# logindemoapi/services/auth_service.py

from login_api.repositories.auth_repository import AuthRepository


class AuthService:
    """
    AuthService is responsible for handling authentication logic.
    It interacts with the AuthRepository to authenticate users.
    """

    def __init__(self, auth_repository: AuthRepository):
        """
        Initializes the AuthService.

        Args:
            auth_repository: An instance of AuthRepository to interact with the database.

        Returns:
            None

        Raises:
            None
        """
        self.auth_repository = auth_repository

    def authenticate(self, email: str, password: str) -> bool:
        """
        Authenticates a user by checking their email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        return self.auth_repository.authenticate_user(email, password)