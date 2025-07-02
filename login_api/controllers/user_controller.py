# logindemoapi/controllers/user_controller.py

from flask import request, jsonify
from login_api.services.user_service import UserService
from login_api.error_handler.exceptions import APIError

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
        """
        data = request.get_json()
        if not data:
            return jsonify({"message": "No input data provided"}), 400

        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        is_active = data.get('is_active', True)

        # Input Validation (Controller's responsibility)
        if not all([email, password]):
            return jsonify({"message": "Missing required fields (email, password)"}), 400
        if not isinstance(email, str) or not email.strip() or "@" not in email:
            return jsonify({"message": "Email must be a valid email address"}), 400
        if not isinstance(password, str) or len(password) < 8:
            return jsonify({"message": "Password must be at least 8 characters long"}), 400
        # Add more validation (e.g., email format regex, password complexity)

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
        except ValueError as e:
            # Business logic errors from service (e.g., duplicate email)
            return jsonify({"message": str(e)}), 409 # 409 Conflict
        except RuntimeError as e:
            # Unexpected system/database errors
            return jsonify({"message": "An internal server error occurred."}), 500
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Unhandled error in UserController.create_user: {e}")
            return jsonify({"message": "An unexpected error occurred."}), 500

    def get_user_by_id(self, user_id: int):
        """
        Handles GET /users/<int:user_id> request to retrieve a single user.
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
            raise APIError("Login failed", 500)

    def get_all_users(self):
        """
        Handles GET /users request to retrieve all users.
        """
        try:
            users_list = self.user_service.get_all_users()
            return jsonify(users_list), 200
        except Exception as e:
            print(f"Unhandled error in UserController.get_all_users: {e}")
            return jsonify({"message": "An unexpected error occurred."}), 500

    def update_user(self, user_id: int):
        """
        Handles PUT /users/<int:user_id> request to update an existing user.
        """
        data = request.get_json()
        if not data:
            return jsonify({"message": "No input data provided"}), 400
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
        except ValueError as e:
            return jsonify({"message": str(e)}), 404
        
    def delete_user(self, user_id: int):
        """
        Handles DELETE /users/<int:user_id> request to delete a user.
        """
        try:
            self.user_service.delete_user(user_id)
            return jsonify({"message": "User deleted successfully"}), 204
        except ValueError as e:
            return jsonify({"message": str(e)}), 404
        except Exception as e:
            print(f"Unhandled error in UserController.delete_user: {e}")
            return jsonify({"message": "An unexpected error occurred."}), 500