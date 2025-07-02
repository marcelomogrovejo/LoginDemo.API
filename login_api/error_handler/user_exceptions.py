# login_api/error_handler/user_exceptions.py 
from login_api.error_handler.exceptions import APIError

# Domain-specific exceptions
class UserNotFoundError(APIError):
    """User not found"""
    def __init__(self, message="User not found"):
        super().__init__(message, 404)

# class AuthenticationError(APIError):
#     """Login failed"""
#     def __init__(self, message="Invalid credentials"):
#         super().__init__(message, 401)
