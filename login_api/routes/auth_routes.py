# logindemoapi/routes/auth_routes.py

from flask import Blueprint
from login_api.controllers.auth_controller import AuthController  # Relative import

# Create a Blueprint instance for auth routes
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

# Placeholder for auth_controller instance (will be injected in main.py)
_auth_controller: AuthController = None

def init_auth_routes(controller: AuthController):
    """
    Initializes the auth routes by injecting the AuthController instance.
    This pattern allows the controller to be created and managed by the app factory.
    """
    global _auth_controller
    _auth_controller = controller

    # Register the routes with the blueprint
    # These methods call the respective controller methods
    auth_bp.add_url_rule('/login', 'login', _auth_controller.login, methods=['POST'])

    return auth_bp