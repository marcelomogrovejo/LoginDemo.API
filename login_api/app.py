# logindemoapi/app.py

from flask import Flask, jsonify
from login_api.config import Config
from login_api.extensions import db
from login_api.repositories.user_repository import UserRepository
from login_api.services.user_service import UserService
from login_api.controllers.user_controller import UserController
from login_api.routes.user_routes import init_user_routes

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

    # --- Set up Database (create tables) ---
    with flask_app.app_context():
        db.create_all() # Creates tables if they don't exist

    # --- Dependency Injection: Build the Layers ---

    # 1. Initialize Repository Layer
    # The UserRepository gets the db.session implicitly from Flask-SQLAlchemy's app context.
    user_repository = UserRepository()

    # 2. Initialize Service Layer (injects repository)
    user_service = UserService(user_repository=user_repository)

    # 3. Initialize Controller Layer (injects service)
    user_controller = UserController(user_service=user_service)

    # 4. Initialize and Register Routes Blueprint (injects controller)
    # The init_user_routes function returns the configured blueprint
    user_routes_blueprint = init_user_routes(controller=user_controller)
    flask_app.register_blueprint(user_routes_blueprint)

    # GET method to retrieve the home page
    @flask_app.route('/')
    def home():
        return jsonify({'message': 'Welcome to the Login Demo API'})

    # --- Global Error Handlers (optional, but good practice) ---
    @flask_app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"message": "Resource not found"}), 404

    @flask_app.errorhandler(500)
    def internal_error(error):
        db.session.rollback() # Ensure rollback on unhandled 500 errors
        return jsonify({"message": "Internal server error"}), 500

    return flask_app

app = create_app()
app.run(debug=True) # debug=True for development, turn off in production
