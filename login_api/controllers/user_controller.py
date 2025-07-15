# logindemoapi/controllers/user_controller.py

from flask import request, jsonify
from login_api.services.user_service import UserService
from login_api.error_handler.exceptions import APIError
from flask_jwt_extended import get_jwt_identity

# You might use a schema validation library here like Marshmallow or Pydantic
# For simplicity, we'll do basic manual validation.

class UserController:
    """
    UserController handles HTTP requests related to user management.
    It validates input, delegates to the UserService, and formats responses.
    """

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user(self):
        """
        Handles POST /users request to create a new user.

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
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        is_active = data.get('is_active', True)

        # Input Validation (Controller's responsibility)
        if not all([email, password]):
            raise APIError("Missing required fields (email, password)", 400)
        if not isinstance(email, str) or not email.strip() or "@" not in email:
            raise APIError("Email must be a valid email address", 400)
        if not isinstance(password, str) or len(password) < 8:
            raise APIError("Password must be at least 8 characters long", 400)

        # TODO: Add more validation (e.g., email format regex, password complexity)

        try:
            # Delegate to the service layer
            user_data = self.user_service.create_user(email, 
                                                      password, 
                                                      first_name,
                                                      last_name,
                                                      is_active)
            return jsonify({
                "message": "User created successfully",
                "user": user_data
            }), 201
        except APIError:
            # Re-raise APIError to be handled by the global error handler
            raise
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Unhandled error in UserController.create_user: {e}")
            raise APIError("An unexpected error occurred while creating the user", 500)

    def get_user_by_id(self, user_id: int):
        """
        Handles GET /users/<int:user_id> request to retrieve a single user.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            JSON response with user data or error message.

        Raises:
            APIError: If the user is not found or if an unexpected error occurs.
        """
        try:
            user_data = self.user_service.get_user_by_id(user_id)
            if not user_data:
                raise APIError("User not found", 404)
            return jsonify(user_data), 200  
        except APIError:
            raise
        except Exception as e:
            print(f"Unhandled error in UserController.get_user_by_id: {e}")
            raise APIError("An unexpected error occurred while retrieving the user", 500)

    def get_all_users(self):
        """
        Handles GET /users request to retrieve all users.

        Args:
            None

        Returns:
            JSON response with a list of users or an error message.

        Raises:
            APIError: If an unexpected error occurs while retrieving users.
        """
        try:
            users_list = self.user_service.get_all_users()
            return jsonify(users_list), 200
        except Exception as e:
            print(f"Unhandled error in UserController.get_all_users: {e}")
            return APIError("An unexpected error occurred while retrieving users", 500)

    def update_user(self, user_id: int):
        """
        Handles PUT /users/<int:user_id> request to update an existing user.

        Args:
            user_id (int): The ID of the user to update.

        Returns:
            JSON response with success message and updated user data or error message.

        Raises:
            APIError: If input validation fails or if an unexpected error occurs.
        """
        data = request.get_json()
        if not data:
            raise APIError("No input data provided", 400)
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        # Input Validation (Controller's responsibility)
        # if not email or not isinstance(email, str) or "@" not in email:
        #     return jsonify({"message": "Email must be a valid email address"}), 400

        try:
            updated_user_data = self.user_service.update_user(user_id, 
                                                              first_name,
                                                              last_name)
            return jsonify({
                "message": "User updated successfully",
                "user": updated_user_data
            }), 200
        except Exception as e:
            print(f"Unhandled error in UserController.update_user: {e}")
            raise APIError("An unexpected error occurred while updating the user", 500)
        
    def delete_user(self, user_id: int):
        """
        Handles DELETE /users/<int:user_id> request to delete a user.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            JSON response with success message or error message.
        
        Raises:
            APIError: If the user is not found or if an unexpected error occurs.
        """
        try:
            self.user_service.delete_user(user_id)
            return jsonify({"message": "User deleted successfully"}), 204
        except Exception as e:
            print(f"Unhandled error in UserController.delete_user: {e}")
            raise APIError("An unexpected error occurred while deleting the user", 500)
    
    # Handles GET /profile request to retrieve the profile of the authenticated user.
    # This method uses JWT to identify the user.
    # It retrieves the user data by email.
    # This method is just exposed for demonstration purposes.
    def profile(self):
        user_email = get_jwt_identity()  # Get user ID from JWT
        user = self.user_service.get_user_by_email(user_email)
        return user