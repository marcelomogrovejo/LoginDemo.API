# logindemoapi/app.py

from flask import Flask, jsonify
from login_api.config import Config
from login_api.extensions import db, bcrypt
from login_api.repositories.user_repository import UserRepository
from login_api.repositories.auth_repository import AuthRepository
from login_api.services.user_service import UserService
from login_api.services.auth_service import AuthService
from login_api.controllers.user_controller import UserController
from login_api.controllers.auth_controller import AuthController
from login_api.routes.user_routes import init_user_routes
from login_api.routes.auth_routes import init_auth_routes
from login_api.error_handler.exceptions import APIError
import sys

def create_app():
    """
    Flask application factory function.
    Initializes the Flask app, configures SQLAlchemy, and sets up the
    dependency graph (repositories -> services -> controllers -> routes).
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config) # Load configuration from Config class

    # Initialize SQLAlchemy with the Flask app
    db.init_app(flask_app)

    # Initialize Flask-Bcrypt for password hashing
    bcrypt.init_app(flask_app)  

    # --- Set up Database (create tables) ---
    with flask_app.app_context():
        db.create_all() # Creates tables if they don't exist

    # --- Dependency Injection: Build the Layers ---

    # 1. Initialize Repository Layer
    # The UserRepository gets the db.session implicitly from Flask-SQLAlchemy's app context.
    user_repository = UserRepository()
    auth_repository = AuthRepository()

    # 2. Initialize Service Layer (injects repository)
    user_service = UserService(user_repository=user_repository)
    auth_service = AuthService(auth_repository=auth_repository)

    # 3. Initialize Controller Layer (injects service)
    user_controller = UserController(user_service=user_service)
    auth_controller = AuthController(auth_service=auth_service)

    # 4. Initialize and Register Routes Blueprint (injects controller)
    # The init_user_routes function returns the configured blueprint
    user_routes_blueprint = init_user_routes(controller=user_controller)
    flask_app.register_blueprint(user_routes_blueprint)

    auth_routes_blueprint = init_auth_routes(controller=auth_controller)
    flask_app.register_blueprint(auth_routes_blueprint)
    
    # GET method to retrieve the home page
    @flask_app.route('/')
    def home():
        return jsonify({'message': 'Welcome to the Login Demo API'})
    
     # Redirect standard output to debug console
    if sys.stdout != sys.__stdout__:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    # Test route
    @flask_app.route('/debug_test')
    def debug_test():
        print("THIS SHOULD APPEAR IN DEBUG CONSOLE")
        return {"status": "success"}

    # --- Global Error Handlers (optional, but good practice) ---
    @flask_app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @flask_app.errorhandler(404)
    def handle_not_found(e):
        return jsonify(message="Resource not found"), 404

    @flask_app.errorhandler(500)
    def handle_server_error(e):
        return jsonify(message="Internal server error"), 500

    return flask_app

app = create_app()
app.run(debug=True) # debug=True for development, turn off in production
