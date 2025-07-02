# logindemoapi/routes/user_routes.py

from flask import Blueprint
from login_api.controllers.user_controller import UserController # Relative import

# Create a Blueprint instance for user routes
user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

# Placeholder for user_controller instance (will be injected in main.py)
_user_controller: UserController = None

def init_user_routes(controller: UserController):
    """
    Initializes the user routes by injecting the UserController instance.
    This pattern allows the controller to be created and managed by the app factory.
    """
    global _user_controller
    _user_controller = controller

    # Register the routes with the blueprint
    # These methods call the respective controller methods
    user_bp.add_url_rule('/', 'create_user', _user_controller.create_user, methods=['POST'])
    user_bp.add_url_rule('/', 'get_all_users', _user_controller.get_all_users, methods=['GET'])
    user_bp.add_url_rule('/<int:user_id>', 'get_user_by_id', _user_controller.get_user_by_id, methods=['GET'])
    user_bp.add_url_rule('/<int:user_id>', 'update_user', _user_controller.update_user, methods=['PUT'])
    user_bp.add_url_rule('/<int:user_id>', 'delete_user', _user_controller.delete_user, methods=['DELETE'])

    return user_bp
