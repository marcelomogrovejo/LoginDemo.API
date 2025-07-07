# logindemoapi/controllers/auth_controller.py

from flask import request, jsonify
from login_api.services.auth_service import AuthService
from login_api.error_handler.exceptions import APIError


class AuthController:
    """
    AuthController handles HTTP requests related to user authentication.
    It validates input, delegates to the AuthService, and formats responses.
    """

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def login(self):
        """
        Handles POST /login request to authenticate a user.

        Args:
            None

        Returns:
            JSON response with success message and user data or error message.

        Raises:
            APIError: If input validation fails or if an unexpected error occurs.
        """
        data = request.get_json()
        if not data:
            raise APIError("No input data provided", 400)

        email = data.get('email')
        password = data.get('password')

        # Input Validation
        if not all([email, password]):
            raise APIError("Missing required fields (email, password)", 400)
        if not isinstance(email, str) or not email.strip() or "@" not in email:
            raise APIError("Email must be a valid email address", 400)
        if not isinstance(password, str) or len(password) < 8:
            raise APIError("Password must be at least 8 characters long", 400)

        try:
            # Delegate to the service layer
            user_data = self.auth_service.authenticate(email, password)
            return jsonify({
                "message": "Login successful",
                "user": user_data,
                "token": "dummy_token",  # Replace with actual token generation logic
                "status": "success"
            }), 200
        except APIError as e:
            raise e
        except Exception as e:
            raise APIError("An unexpected error occurred", 500) from e
